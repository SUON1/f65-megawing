#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "m1_graphics.h"
#include "m1_input.h"

static uint32_t baseline[601];

static uint32_t replay(uint8_t divisor)
{
    M1Core core;
    M1Snapshots pool = {0};
    M1Input input = {0};
    M1Graphics graphics = {0};
    uint8_t stages[M1_STAGES];
    uint8_t row[M1_COLUMNS];
    uint32_t history[601] = {0};
    m1_core_init(&core);
    for (uint32_t i = 0u; i < 600u; ++i)
    {
        assert(m1_input_sample(&input, &core, (uint8_t)((i / 25u) & 1u)));
        m1_tick(&core, &pool, stages);
        history[core.tick] = core.checksum;
        if (divisor == 0u)
        {
            baseline[core.tick] = core.checksum;
        }
        else
        {
            assert(core.checksum == baseline[core.tick]);
        }
        for (uint8_t stage = 0u; stage < M1_STAGES; ++stage)
        {
            assert(stages[stage] == stage + 1u);
        }
        if (divisor != 0u && i % divisor == 0u)
        {
            uint8_t slot = m1_acquire(&pool);
            assert(slot < M1_SNAPSHOT_SLOTS);
            assert(pool.slots[slot].tick <= core.tick);
            assert(pool.slots[slot].checksum == history[pool.slots[slot].tick]);
            assert(m1_render_begin(&graphics, &pool.slots[slot]));
            m1_release(&pool, slot);
            while (!graphics.ready)
            {
                m1_render_row(&graphics, row);
                m1_render_advance(&graphics);
            }
            assert(m1_render_commit(&graphics));
        }
    }
    assert(core.tick == 600u && core.commands == 23u && core.fault == 0u);
    return core.checksum;
}

int main(void)
{
    // Independently check the required white overlay, blue sky and green ground.
    uint8_t colors[M1_COLUMNS];
    for (uint8_t row = 0u; row < M1_ROWS; ++row)
    {
        assert(m1_render_colors(row, colors));
        uint8_t expected_color = row < 9u ? 1u : (row < 13u ? 6u : 5u);
        for (uint8_t column = 0u; column < M1_COLUMNS; ++column)
        {
            assert(colors[column] == expected_color);
        }
    }
    memset(colors, 0xa5, sizeof(colors));
    assert(!m1_render_colors(M1_ROWS, colors));
    for (uint8_t column = 0u; column < M1_COLUMNS; ++column)
    {
        assert(colors[column] == 0xa5u);
    }
    uint32_t expected = replay(0u);
    assert(replay(1u) == expected && replay(3u) == expected && replay(17u) == expected);
    M1Core core;
    m1_core_init(&core);
    for (uint8_t i = 0u; i < M1_QUEUE_CAPACITY; ++i)
    {
        M1Command command = {(uint32_t)i + 1u, 1u, 0u};
        assert(m1_command(&core, command));
    }
    M1Command saved[M1_QUEUE_CAPACITY];
    memcpy(saved, core.queue, sizeof(saved));
    M1Command extra = {20u, 1u, 0u};
    assert(!m1_command(&core, extra));
    assert(core.count == M1_QUEUE_CAPACITY && memcmp(saved, core.queue, sizeof(saved)) == 0);
    m1_core_init(&core);
    M1Command invalid = {1u, 2u, 0u};
    assert(!m1_command(&core, invalid) && core.count == 0u);
    invalid.pressed = 1u;
    invalid.released = 1u;
    assert(!m1_command(&core, invalid) && core.count == 0u);

    M1Snapshots pool = {0};
    M1Snapshot value = {1u, 2u, 3u, 0u};
    assert(m1_publish(&pool, &value));
    uint8_t held = m1_acquire(&pool);
    for (uint8_t i = 1u; i < M1_SNAPSHOT_SLOTS; ++i)
    {
        value.tick++;
        assert(m1_publish(&pool, &value));
    }
    M1Snapshot original = pool.slots[held];
    assert(!m1_publish(&pool, &value));
    assert(memcmp(&original, &pool.slots[held], sizeof(original)) == 0);
    uint8_t latest = m1_acquire(&pool);
    assert(latest != held && pool.slots[latest].tick == 3u && pool.state[held] == 2u);
    m1_release(&pool, held);

    M1Graphics graphics = {0};
    assert(m1_render_begin(&graphics, &value));
    assert(!m1_render_commit(&graphics));
    m1_render_advance(&graphics);
    m1_render_cancel(&graphics);
    assert(!m1_render_commit(&graphics) && graphics.generation == 0u);
    assert(m1_render_begin(&graphics, &value));
    for (uint8_t i = 0u; i < M1_ROWS; ++i)
    {
        m1_render_advance(&graphics);
    }
    assert(m1_render_commit(&graphics));
    assert(!m1_render_begin(&graphics, &value));
    printf("M1 HOST PASS: colors, stages, queue, input edges, held reader, rejection, cancellation, replay %08X\n", expected);
    return 0;
}
