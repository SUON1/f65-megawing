// Early complete-renderer link. NOT admitted for execution or full target fit.
// Real renderer/assets/state and mutable semantic camera; opaque backend only.
// Display initialization/adapter and service deadlines await later gates.
#include "camera.h"
#include "m1_input.h"
#include "m1_platform.h"
#include "m1_snapshot.h"
#include "m2_camera_input.h"
#include "m2_renderer.h"

extern uint16_t m2_fit_camera_keys(void);
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
    uint32_t release = m1_platform_now();
    uint32_t period = m1_platform_period() >> 16u;
    for (;;)
    {
        uint32_t now = m1_platform_now();
        if ((int32_t)(now - release) >= 0)
        {
            if (!m1_input_sample(&input, &core, m1_platform_key()))
            {
                break;
            }
            m1_tick(&core, &snapshots, stages);
            release += period;
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
            uint8_t slot = m1_acquire(&snapshots);
            if (slot < M1_SNAPSHOT_SLOTS)
            {
                M1Snapshot source = snapshots.slots[slot];
                m1_release(&snapshots, slot);
                if (renderer.phase == M2_RENDER_IDLE)
                {
                    (void)m2_renderer_begin(&renderer, &requested, &source, core.tick);
                }
            }
            m2_renderer_service(&renderer, requested.revision);
            if (renderer.phase == M2_RENDER_READY)
            {
                (void)m2_renderer_commit(&renderer, requested.revision);
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
