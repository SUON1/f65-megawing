// Host-only mutable instruction data exposes actual fail-closed decoder paths.
// The interpreter source is included once, not copied or reimplemented.
#define M2_COMMAND_TEST_DATA
#include "m2_compact.c"

#include <assert.h>
#include <stddef.h>
#include <stdio.h>

#include "camera.h"
#include "m2_raster_private.h"
#include "m2_rebuild.h"
#include "m2_record_private.h"

static void rejected(M2Compact *work, struct M2Prepared *prepared)
{
    M2Line output;
    memset(&output, 0xA5, sizeof(output));
    M2Line before = output;
    assert(m2_command_service(work, prepared, 0, &output) == -1);
    assert(memcmp(&output, &before, sizeof(output)) == 0);
}

static void negative_commands(struct M2Prepared *prepared)
{
    M2Compact work;
    uint8_t saved[4];
    memcpy(saved, m2_commands[M2P_PROJECT], 4u);
    static const uint8_t bad[][4] = {
        {7,0,0,0}, {255,0,0,0}, {M2V_COPY,127,128,0},
        {M2V_COPY,128,0,0}, {M2V_JUMP,0,M2P_PREPARE,0},
        {M2V_NEXT,3,2,M2P_PROJECT}, {M2V_NEXT,0,0,M2P_PROJECT},
        {M2V_RETURN,0,0,0}, {M2V_DIV_SET,11,0,30},
        {(uint8_t)(M2V_MUL_ADD ^ 32u),10,0,13},
        {M2V_DONE,1,0,0}
    };
    for (uint8_t i = 0u; i < sizeof(bad) / sizeof(bad[0]); ++i)
    {
        memset(&work, 0, sizeof(work));
        start(&work, 1u);
        memcpy(m2_commands[M2P_PROJECT], bad[i], 4u);
        rejected(&work, prepared);
    }
    memcpy(m2_commands[M2P_PROJECT], saved, 4u);
    start(&work, 1u);
    work.state = 255u;
    rejected(&work, prepared);
    start(&work, 1u);
    work.counters[0] = 2u;
    rejected(&work, prepared);
    start(&work, 1u);
    work.state = (uint8_t)(M2P_AXIS + 1u);
    work.waiting = 1u;
    work.job.phase = 0u;
    rejected(&work, prepared);
    start(&work, 1u);
    work.state = M2P_INTERPOLATE;
    work.return_active = 1u;
    work.outside = 2u;
    work.inside = 1u;
    rejected(&work, prepared);
    start(&work, 1u);
    M2Line output;
    assert(m2_command_service(&work, prepared, 0, &output) == 0);
    M2Compact moved = work;
    rejected(&moved, prepared);
    struct M2Prepared changed_binding = *prepared;
    rejected(&work, &changed_binding);
    // An explicit restart safely rebinds a moved context.
    start(&moved, 1u);
    assert(m2_command_service(&moved, prepared, 0, &output) == 0);
    puts("COMMAND NEGATIVES PASS: unknown opcode, PC, operands, constant destination, branch, counter, return, product/phase, alias and completion kind");
}

static void metadata(struct M2Prepared *prepared)
{
    M2RebuildRenderer renderer = {0};
    renderer.prepared = *prepared;
    renderer.destination = 1u;
    renderer.generation = 7u;
    renderer.snapshot.tick = 42u;
    renderer.snapshot.checksum = 0x12345678u;
    renderer.tile_index = 960u;
    assert(m2_bundle_fields(&renderer, 0u));
    assert(m2_bundle_fields(&renderer, 1u));
    uint8_t mask[sizeof(M2RebuildBundle)] = {0};
    static const uint8_t spans[][2] = {
        {offsetof(M2RebuildBundle, registration.camera),18},
        {offsetof(M2RebuildBundle, registration.camera.revision),4},
        {offsetof(M2RebuildBundle, registration.transform),72},
        {offsetof(M2RebuildBundle, registration.generation),4},
        {offsetof(M2RebuildBundle, registration.source_tick),4},
        {offsetof(M2RebuildBundle, registration.fixture_revision),4},
        {offsetof(M2RebuildBundle, registration.projection_revision),4},
        {offsetof(M2RebuildBundle, registration.composition_revision),4},
        {offsetof(M2RebuildBundle, registration.view_id),2},
        {offsetof(M2RebuildBundle, registration.tier_id),2},
        {offsetof(M2RebuildBundle, registration.store),1},
        {offsetof(M2RebuildBundle, composition_revision),4},
        {offsetof(M2RebuildBundle, checksum),4}
    };
    for (uint8_t i = 0u; i < sizeof(spans) / sizeof(spans[0]); ++i)
    {
        memset(mask + spans[i][0], 1, spans[i][1]);
    }
    uint16_t checked = 0u;
    for (size_t byte = 0u; byte < sizeof(mask); ++byte)
    {
        uint8_t *candidate = (uint8_t *)&renderer.bundles[1];
        candidate[byte] ^= 1u;
        M2RebuildRenderer before = renderer;
        assert(m2_bundle_fields(&renderer, 1u) == !mask[byte]);
        assert(memcmp(&renderer, &before, sizeof(renderer)) == 0);
        candidate[byte] ^= 1u;
        checked += mask[byte];
    }
    assert(checked == 127u);
    assert(!m2_bundle_fields(&renderer, 2u));
    renderer.tile_index = 959u;
    assert(!m2_bundle_fields(&renderer, 1u));
    renderer.tile_index = 960u;
    renderer.prepared.ready = 0u;
    assert(!m2_bundle_fields(&renderer, 0u));
    renderer.prepared.ready = 1u;
    renderer.generation = 0u;
    assert(!m2_bundle_fields(&renderer, 0u));
    renderer.generation = 1u;
    renderer.destination = 2u;
    assert(!m2_bundle_fields(&renderer, 0u));
    printf("METADATA PASS: %u protected field bytes reject corruption; ABI padding ignored; comparison read-only; invalid capture/mode/store/completion fail\n", checked);
}

static void raster_failures(void)
{
    struct M2RasterCursor cursor;
    memset(&cursor, 0xA5, sizeof(cursor));
    struct M2RasterCursor before = cursor;
    for (uint8_t field = 0u; field < 4u; ++field)
    {
        int32_t extent = field < 2u ? M2_WIDTH : M2_HEIGHT;
        int32_t invalid[2] = {-(int32_t)M2_SCREEN_SCALE / 2 - 1,
            extent * (int32_t)M2_SCREEN_SCALE - (int32_t)M2_SCREEN_SCALE / 2 + 1};
        for (uint8_t side = 0u; side < 2u; ++side)
        {
            M2Line line = {{0,0},{0,0}};
            memcpy((uint8_t *)&line + field * sizeof(int32_t), &invalid[side], sizeof(int32_t));
            assert(!m2_raster_begin(&line, &cursor));
            assert(memcmp(&cursor, &before, sizeof(cursor)) == 0);
        }
    }
    puts("RASTER NEGATIVES PASS: both bounds on all four coordinates; cursor unchanged");
}

int main(void)
{
    M2Camera camera;
    m2rb_camera_init(&camera);
    struct M2Prepared prepared;
    assert(m2_prepare(&prepared, &camera));
    negative_commands(&prepared);
    metadata(&prepared);
    raster_failures();
    return 0;
}
