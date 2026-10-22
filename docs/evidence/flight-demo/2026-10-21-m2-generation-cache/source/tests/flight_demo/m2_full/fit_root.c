// Early complete-renderer link. NOT admitted for execution or full target fit.
// Real renderer/assets/state and mutable semantic camera; opaque backend only.
// Display adapter and actual service bounds await admission; unknown bounds stall work.
#include "camera.h"
#include "dispatch.h"
#include "m1_input.h"
#include "m1_platform.h"
#include "m1_snapshot.h"
#include "m2_camera_input.h"
#include "m2_renderer.h"

extern uint16_t m2_fit_camera_keys(void);
extern uint32_t m2_fit_service_bound(uint8_t action);
extern uint32_t m2_fit_return_margin(void);
static M1Core core;
static M1Snapshots snapshots;
static M1Input input;
static M2Camera requested;
static uint16_t previous_camera_keys;
static M2Renderer renderer;
static uint8_t stages[M1_STAGES];

int main(void)
{
    if (!m1_platform_begin())
    {
        m1_platform_alarm();
        for (;;) {}
    }
    m1_core_init(&core);
    m2_camera_reset(&requested);
    m2_renderer_init(&renderer);
    M2Dispatch dispatch = {m1_platform_now(), 0u};
    uint32_t period = m1_platform_period();
    for (;;)
    {
        uint32_t now = m1_platform_now();
        if ((uint32_t)(now - dispatch.release) < 0x80000000ul)
        {
            if (!m1_input_sample(&input, &core, m1_platform_key()))
            {
                break;
            }
            m1_tick(&core, &snapshots, stages);
            m2_dispatch_next(&dispatch, period);
            uint16_t pressed = m2_camera_pressed(&previous_camera_keys, m2_fit_camera_keys());
            if (!m2_camera_command(&requested, pressed))
            {
                if (renderer.faults == UINT32_MAX)
                {
                    break;
                }
                ++renderer.faults;
            }
        }
        else
        {
            // Each action includes its complete callees. Zero/unknown bounds
            // grant no work; real admission has not supplied this backend.
            uint8_t action = renderer.phase == M2_RENDER_IDLE
                             ? (uint8_t)(M2_RENDER_FATAL + 1u) : renderer.phase;
            uint32_t bound = m2_fit_service_bound(action);
            uint32_t margin = m2_fit_return_margin();
            if (m2_dispatch_allows(m1_platform_now(), dispatch.release, bound, margin))
            {
                if (renderer.phase == M2_RENDER_IDLE)
                {
                    uint8_t slot = m1_acquire(&snapshots);
                    if (slot < M1_SNAPSHOT_SLOTS)
                    {
                        M1Snapshot source = snapshots.slots[slot];
                        m1_release(&snapshots, slot);
                        (void)m2_renderer_begin(&renderer, &requested, &source, core.tick);
                    }
                }
                else if (renderer.phase == M2_RENDER_READY)
                {
                    (void)m2_renderer_commit(&renderer, requested.revision);
                }
                else
                {
                    m2_renderer_service(&renderer, requested.revision);
                }
            }
        }
        if (m1_platform_fault() || renderer.phase == M2_RENDER_FATAL || core.fault)
        {
            break;
        }
        m1_platform_measure();
    }
    m1_platform_alarm();
    for (;;) {}
}
