// Graphics-owned private construction state. No hardware or physical pointers.
#pragma once
#include "m2_full.h"
#include "m2_prepared_private.h"
#include "m2_raster_private.h"

enum M2RenderPhase
{
    M2_RENDER_IDLE, M2_RENDER_PREPARE, M2_RENDER_REGISTER,
    M2_RENDER_ANCHOR, M2_RENDER_TELEMETRY, M2_RENDER_BACKGROUND,
    M2_RENDER_CACHE, M2_RENDER_SEGMENT, M2_RENDER_RASTER,
    M2_RENDER_OVERLAY, M2_RENDER_TRANSFER, M2_RENDER_READY, M2_RENDER_FATAL
};

// Target has 272 line bytes + 17 visibility bytes = 289; native padding may differ.
struct M2ProjectionCache
{
    M2Line lines[M2_SEGMENT_COUNT];
    uint8_t visible[M2_SEGMENT_COUNT];
};

union M2ConstructionWorkspace
{
    char text[320];
    struct M2ProjectionCache cache;
};
_Static_assert(sizeof(struct M2ProjectionCache) <= 320u, "cache exceeds workspace");
_Static_assert(sizeof(union M2ConstructionWorkspace) == 320u, "workspace changed");
#ifdef M2_TARGET_LAYOUT_CHECK
_Static_assert(sizeof(struct M2ProjectionCache) == 289u, "target cache layout changed");
#endif

typedef struct
{
    M2Bundle bundles[2];
    struct M2Prepared prepared;
    M1Snapshot source;
    struct M2RasterCursor cursor;
    M2Line line;
    uint8_t tile[M2_FULL_TILE_BYTES];
    union M2ConstructionWorkspace workspace;
    uint32_t cache_generation;
    uint32_t cache_revision;
    uint32_t sampled_tick;
    uint32_t generation;
    uint32_t cancellations;
    uint32_t faults;
    uint16_t tile_index;
    uint8_t sample;
    uint8_t segment;
    uint8_t displayed;
    uint8_t pending;
    uint8_t has_display;
    uint8_t phase;
} M2Renderer;

// Backend synchronous completion: copied bytes no longer borrowed on return.
// Only dispatcher calls these seams; no concurrent publication or IRQ readers.
uint8_t m2_backend_tile(uint8_t store, uint16_t index, const uint8_t *bytes);
uint8_t m2_backend_activate(uint8_t store);

void m2_renderer_init(M2Renderer *renderer);
uint8_t m2_renderer_begin(M2Renderer *renderer, const M2Camera *camera,
                          const M1Snapshot *snapshot, uint32_t tick);
// Dispatcher must admit the entire phase/callees before calling this primitive.
void m2_renderer_service(M2Renderer *renderer, uint32_t wanted_revision);
uint8_t m2_renderer_commit(M2Renderer *renderer, uint32_t wanted_revision);
void m2_renderer_cancel(M2Renderer *renderer);
// Equal priority for corners in this profile; stable ID is the tie-breaker.
void m2_label_offer(M2Bundle *bundle, uint8_t corner);
uint8_t m2_font_row(char character, uint8_t row);
