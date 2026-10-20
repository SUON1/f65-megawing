// M1 development composition root. No flight or gameplay owner is enabled.
#include "m1_graphics.h"
#include "m1_input.h"
#include "m1_platform.h"

#ifndef M1_REPLAY
#define M1_REPLAY 0
#endif
#ifndef M1_RENDER_DIVISOR
#define M1_RENDER_DIVISOR 1u
#endif

M1Core m1_core;
M1Snapshots m1_snapshots;
M1Graphics m1_graphics;
M1Input m1_input;
uint8_t m1_stages[M1_STAGES];
volatile uint32_t m1_debt_max;
volatile uint32_t m1_display_age;
volatile uint32_t m1_replay_checksum;
volatile uint32_t m1_replay_tick;
volatile uint8_t m1_status;
volatile uint32_t m1_current_tick;
volatile uint32_t m1_display_generation;
volatile uint32_t m1_source_tick;
volatile uint8_t m1_display_store;
static uint8_t row[M1_COLUMNS];

static void stop_with_fault(uint8_t reason)
{
    m1_status = reason;
    m1_platform_alarm();
    for (;;)
    {
    }
}

int main(void)
{
    m1_status = 1u;
    if (!m1_platform_begin())
    {
        stop_with_fault(255u);
    }
    for (uint8_t color_row = 0u; color_row < M1_ROWS; ++color_row)
    {
        if (!m1_render_colors(color_row, row)
            || !m1_platform_color_row(color_row, row))
        {
            stop_with_fault(255u);
        }
    }
    m1_platform_palette(M1_SCENE_BORDER, M1_SCENE_BACKGROUND);
    m1_core_init(&m1_core);
    uint32_t release = m1_platform_now();
    uint32_t period = m1_platform_period();
    uint16_t fraction = 0u;
    uint8_t render_counter = 0u;
    m1_status = 2u;
    for (;;)
    {
        if (m1_platform_fault())
        {
            stop_with_fault(254u);
        }
        uint32_t now = m1_platform_now();
        if ((uint32_t)(now - release) < 0x80000000ul)
        {
            uint32_t debt = now - release;
            if (debt > m1_debt_max)
            {
                m1_debt_max = debt;
            }
            uint8_t down = M1_REPLAY
                           ? (uint8_t)((m1_core.tick / 25u) & 1u)
                           : m1_platform_key();
            (void)m1_input_sample(&m1_input, &m1_core, down);
            m1_tick(&m1_core, &m1_snapshots, m1_stages);
            m1_current_tick = m1_core.tick;
            uint32_t next = (uint32_t)fraction + (period & 65535u);
            release += (period >> 16u) + (next >> 16u);
            fraction = (uint16_t)next;
            if (m1_core.tick == 600u)
            {
                m1_replay_checksum = m1_core.checksum;
                m1_replay_tick = m1_core.tick;
                m1_platform_measure();
            }
            // A delayed dispatcher catches up in order. Never render ahead of debt.
            continue;
        }
        if (!m1_graphics.busy)
        {
            uint8_t slot = m1_acquire(&m1_snapshots);
            if (slot != M1_SNAPSHOT_SLOTS)
            {
                m1_graphics.sampled_tick = m1_core.tick;
                m1_graphics.sampled_debt = m1_debt_max;
                m1_graphics.published = m1_core.tick - m1_snapshots.rejected;
                (void)m1_render_begin(&m1_graphics, &m1_snapshots.slots[slot]);
                m1_release(&m1_snapshots, slot);
            }
        }
        if (m1_graphics.busy && !m1_graphics.ready)
        {
            ++render_counter;
            if (render_counter >= M1_RENDER_DIVISOR)
            {
                render_counter = 0u;
                m1_render_row(&m1_graphics, row);
                if (!m1_platform_row(m1_graphics.destination, m1_graphics.row, row))
                {
                    stop_with_fault(253u);
                }
                m1_render_advance(&m1_graphics);
                if (m1_graphics.ready)
                {
                    // Arm on completion; only the next fresh frame may swap.
                    (void)m1_platform_frame();
                }
            }
        }
        if (m1_graphics.ready && m1_platform_frame())
        {
            if (!m1_platform_swap(m1_graphics.destination)
                || !m1_render_commit(&m1_graphics))
            {
                stop_with_fault(252u);
            }
        }
        m1_display_generation = m1_graphics.generation;
        m1_source_tick = m1_graphics.displayed_tick;
        m1_display_store = m1_graphics.displayed_store;
        m1_display_age = m1_core.tick - m1_graphics.displayed_tick;
    }
}
