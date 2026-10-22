// Compile-only opaque backend. NO hardware access and NOT a display adapter.
// Build without LTO so the target root cannot specialize away renderer work.
// Its mailbox/staging costs are charged as test scaffolding, not real scanout.
#include "m2_renderer.h"

volatile uint16_t m2_fit_camera_down;
volatile uint8_t m2_fit_copy_ok = 1u;
volatile uint8_t m2_fit_activate_ok = 1u;
volatile uint8_t m2_fit_store;
volatile uint16_t m2_fit_tile;
volatile uint8_t m2_fit_staging[64];

uint16_t m2_fit_camera_keys(void)
{
    return m2_fit_camera_down;
}

uint8_t m2_backend_tile(uint8_t store, uint16_t index, const uint8_t *bytes)
{
    m2_fit_store = store;
    m2_fit_tile = index;
    for (uint8_t i = 0u; i < 64u; ++i)
    {
        m2_fit_staging[i] = bytes[i];
    }
    return m2_fit_copy_ok;
}

uint8_t m2_backend_activate(uint8_t store)
{
    m2_fit_store = store;
    return m2_fit_activate_ok;
}

// Zero is unadmitted. Volatile/opaque inputs keep the compile-only paths live;
// synthetic host grants do not qualify as target cycle/service proof.
volatile uint32_t m2_fit_service_ticks;
volatile uint32_t m2_fit_return_ticks;
uint32_t m2_fit_service_bound(uint8_t action)
{
    (void)action;
    return m2_fit_service_ticks;
}
uint32_t m2_fit_return_margin(void)
{
    return m2_fit_return_ticks;
}
