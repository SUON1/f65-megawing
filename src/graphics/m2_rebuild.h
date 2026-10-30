// Graphics owns this private workspace. No aliasing, public ABI or serialization.
#pragma once
#include "m1_snapshot.h"
#include "m2_compact.h"
#include "m2_prepared_private.h"
#include "m2_raster_private.h"
#include "m2_rebuild_profile.h"

enum
{
    M2RB_BEGIN, M2RB_PREPARE, M2RB_PROJECT, M2RB_BACKGROUND,
    M2RB_COPY, M2RB_LINE, M2RB_TEXT, M2RB_COMMIT, M2RB_FAILED
};

typedef struct M2RebuildRenderer
{
    struct M2Prepared prepared;
    M2Compact geometry;
    M2Horizon horizon;
    M2Line lines[M2RB_SEGMENTS];
    M2RebuildBundle bundles[2];
    M1Snapshot snapshot;
    struct M2RasterCursor raster;
    uint32_t generation;
    uint32_t prepared_count;
    uint32_t projected_count;
    uint32_t cancellations;
    uint32_t rejected;
    uint32_t commits;
    uint32_t source_age_at_text;
    uint16_t tile_index;
    uint16_t pending_offset;
    uint8_t visible[M2RB_SEGMENTS];
    uint8_t tile[64];
    char text[40];
    uint8_t phase;
    uint8_t after_copy;
    uint8_t tile_row;
    uint8_t segment;
    uint8_t raster_active;
    uint8_t front;
    uint8_t destination;
    uint8_t shown;
    uint8_t fault;
    uint8_t preparing_horizon;
    uint8_t geometry_active;
} M2RebuildRenderer;

void m2rb_renderer_init(M2RebuildRenderer *renderer);
// A zero budget refuses all work. Positive host grants do not admit target cost.
// The caller must prove the whole selected operation fits before its deadline.
// current_tick is an immutable copy of the authoritative tick, never a new clock.
uint8_t m2rb_dispatch(M2RebuildRenderer *renderer, M1Snapshots *pool,
                       const M2Camera *wanted, uint32_t admitted_budget,
                       uint32_t current_tick);
// Pure telemetry formatter and glyph builder, also independently inspected by tests.
void m2rb_text_row(M2RebuildRenderer *renderer, uint8_t row);
void m2rb_glyph(char character, uint8_t pixels[64]);
