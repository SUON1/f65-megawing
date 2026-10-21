// Compile-only integrated reachability probe. Never admitted for execution.
// No display activation; this precedes the resumable renderer and mode contract.
#include "m1_input.h"
#include "m1_snapshot.h"
#include "m1_platform.h"
#include "m2_fixture.h"
#include "m2_geometry.h"
#include "m2_raster_private.h"

static M1Core core;
static M1Input input;
static M1Snapshots snapshots;
static uint8_t stages[M1_STAGES];
static M2Camera camera = {{{-4500L * M2_POSITION_SCALE, 0,
                          -300L * M2_POSITION_SCALE}}, 0, -5, 0, 1u};
static M2Registration registration;
static M2Point first;
static M2Point last;
static M2Surface surface;
static M2Line line;
// One Graphics-owned continuation plus one output sample.
static struct M2RasterCursor cursor;
static M2Pixel pixel;
static uint16_t count;
volatile uint8_t m2_fit_index;
volatile uint32_t m2_fit_digest;

static void consume(const void *data, uint16_t size)
{
    const uint8_t *bytes = data;
    for (uint16_t i = 0u; i < size; ++i)
    {
        m2_fit_digest = (m2_fit_digest * 33u) ^ bytes[i];
    }
}

int main(void)
{
    if (!m1_platform_begin())
    {
        m1_platform_alarm();
        for (;;) {}
    }
    m1_core_init(&core);
    m2_fit_digest = m1_platform_period();
    m2_fit_digest ^= m1_platform_now();
    m2_fit_digest ^= m1_input_sample(&input, &core, m1_platform_key());
    m1_tick(&core, &snapshots, stages);
    uint8_t slot = m1_acquire(&snapshots);
    if (slot != M1_SNAPSHOT_SLOTS)
    {
        m2_fit_digest ^= m2_registration(&camera, 1u,
                                         snapshots.slots[slot].tick, 0u,
                                         &registration);
        m1_release(&snapshots, slot);
    }
    m2_fit_digest ^= m2_fixture_segment(1u, m2_fit_index, &first, &last);
    m2_fit_digest ^= m2_surface_query(1u, &first, &surface);
    m2_fit_digest ^= (uint8_t)m2_project_segment(&camera, &first, &last, &line);
    count = 0u;
    if (m2_raster_begin(&line, &cursor))
    {
        while (m2_raster_next(&cursor, &pixel))
        {
            consume(&pixel, sizeof(pixel));
            ++count;
        }
    }
    m2_fit_digest ^= (uint8_t)m2_ground_sample(&camera, m2_fit_index, 0u);
    m2_fit_digest ^= m2_pair_eligible(&registration, &registration, 1u, 1u);
    consume(&core, sizeof(core));
    consume(&snapshots, sizeof(snapshots));
    consume(&registration, sizeof(registration));
    consume(&surface, sizeof(surface));
    consume(&line, sizeof(line));

    consume(&count, sizeof(count));
    m1_platform_measure();
    m2_fit_digest ^= m1_platform_fault();
    // Reset-only lifecycle: no C runtime/ROM return is reachable.
    for (;;) {}
}
