// Complete, deliberately unadmitted target composition. No banking or flight.
#include "camera.h"
#include "guard.h"
#include "m1_input.h"
#include "m1_platform.h"
#include "m2_rebuild.h"
#include "platform.h"

static M1Core core;
static M1Snapshots snapshots;
static M1Input input;
static M2RebuildInput camera_input;
static M2Camera camera;
static M2RebuildRenderer renderer;
static uint8_t stages[M1_STAGES];

// Volatile reads retain the whole real application in the link. These are NOT
// an enabling interface: no source path writes them or admits this executable.
volatile uint8_t m2rb_launch_authorized;
volatile uint32_t m2rb_target_budgets[8];
volatile uint32_t m2rb_guard_budget;
volatile uint8_t m2rb_status;
volatile uint32_t m2rb_replay_checkpoint;

static void stop(uint8_t reason)
{
    m2rb_status = reason;
    for (;;)
    {
    }
}

int main(void)
{
    if (m2rb_launch_authorized != 1u)
    {
        stop(1u);
    }
    if (!m1_platform_begin() || !m2rb_platform_init())
    {
        stop(255u);
    }
    m1_core_init(&core);
    m2rb_camera_init(&camera);
    m2rb_renderer_init(&renderer);
    uint32_t release = m1_platform_now();
    uint32_t period = m1_platform_period();
    uint16_t fraction = 0u;
    for (;;)
    {
        if (m1_platform_fault() || renderer.fault != 0u)
        {
            stop(254u);
        }
        uint32_t now = m1_platform_now();
        if ((uint32_t)(now - release) < 0x80000000UL)
        {
            // Catch up one ordered tick at a time; no skipped/merged releases.
            uint16_t edges = m2rb_input_edges(&camera_input, m2rb_platform_keys());
            if (m2rb_camera_edges(&camera, edges) < 0)
            {
                stop(253u);
            }
            (void)m1_input_sample(&input, &core, m1_platform_key());
            m1_tick(&core, &snapshots, stages);
            uint32_t next = (uint32_t)fraction + (period & 65535u);
            release += (period >> 16u) + (next >> 16u);
            fraction = (uint16_t)next;
            if (core.tick == 600u)
            {
                m2rb_replay_checkpoint = core.checksum;
            }
            if (core.tick == 0xffffffffUL)
            {
                stop(252u);
            }
            continue;
        }
        uint8_t slot = renderer.phase;
        if (slot >= 8u)
        {
            stop(251u);
        }
        uint32_t budget = m2rb_target_budgets[slot];
        if (m2rb_guard(now, release, budget, m2rb_guard_budget))
        {
            (void)m2rb_dispatch(&renderer, &snapshots, &camera, budget, core.tick);
        }
    }
}
