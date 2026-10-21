// Pure development geometry. No hardware access or display activation.
#pragma once
#include "m2_pr1.h"

uint8_t m2_camera_valid(const M2Camera *camera);
uint8_t m2_transform(const M2Camera *camera, M2Transform *transform);
// 1 visible, 0 clipped empty, -1 invalid; output unchanged unless visible.
int8_t m2_project_segment(const M2Camera *camera, const M2Point *first,
                          const M2Point *last, M2Line *line);
// Bounded Bresenham samples; capacity failure leaves output/count unchanged.
uint8_t m2_raster_line(const M2Line *line, M2Pixel *pixels,
                        uint16_t capacity, uint16_t *count);
// Downward world ray is ground (1); horizontal/upward ray is sky (0).
int8_t m2_ground_sample(const M2Camera *camera, uint16_t x, uint16_t y);
// Immutable by caller contract after construction. No display state mutation.
uint8_t m2_registration(const M2Camera *camera, uint32_t generation,
                         uint32_t source_tick, uint8_t store,
                         M2Registration *record);
// Pure eligibility predicate. Caller must latch wanted revision and completion
// at the actual PR2 commit boundary; this does not implement that boundary.
uint8_t m2_pair_eligible(const M2Registration *world,
                          const M2Registration *record,
                          uint32_t wanted_camera_revision, uint8_t complete);

// Graphics-private transient cursor, not a generated/public record layout.
// Callers retain exclusive ownership; only begin/next may mutate it.
struct M2RasterCursor;
// Failed begin leaves the cursor unchanged; do not consume a failed attempt.
uint8_t m2_raster_begin(const M2Line *line, struct M2RasterCursor *cursor);
// Requires a successfully initialized, unmodified cursor. At most one pixel.
// Empty/null leaves the output unchanged; exhausted cursors remain exhausted.
uint8_t m2_raster_next(struct M2RasterCursor *cursor, M2Pixel *pixel);
