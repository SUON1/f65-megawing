#ifndef R0FG1_PRESENTATION_H
#define R0FG1_PRESENTATION_H

#include <stdint.h>

#include "r0f_group1_presentation.h"

// Private native C state, not a public/serialized WorldRegistrationRecord.
// Owns no global state, registers, physical memory, clocks, DMA or interrupts.
// Caller supplies non-null pointers and initialized state owned by this module.
typedef struct
{
    uint16_t generation;
    uint16_t source_tick;
    uint8_t view;
    uint8_t tier;
    uint8_t buffer;
} r0fg1_presentation_key;

typedef struct
{
    uint16_t handle;
    uint16_t x;
    uint16_t y;
    uint8_t priority;
} r0fg1_anchor;

typedef struct
{
    r0fg1_presentation_key key;
    r0fg1_anchor anchors[R0FG1P_ANCHORS];
    uint16_t terrain_y[R0FG1P_OCCLUSION_COLUMNS];
    uint16_t terrain_depth[R0FG1P_OCCLUSION_COLUMNS];
    int16_t horizon;
    uint8_t anchor_count;
    uint8_t column_mask;
    uint8_t column_count;
} r0fg1_registration;

typedef struct
{
    r0fg1_registration building;
    r0fg1_registration displayed;
    uint16_t completions;
    uint16_t swaps;
    uint16_t anchor_drops;
    uint8_t requested_view;
    uint8_t composition_view;
    uint8_t busy;
    uint8_t ready;
    uint8_t displayed_valid;
    uint8_t anchor_high;
    uint8_t occlusion_high;
} r0fg1_presentation;

enum
{
    R0FG1P_INVALID = 0,
    R0FG1P_RETAINED = 1,
    R0FG1P_DROPPED = 2,
    R0FG1P_UNCLIPPED = 1,
    R0FG1P_CLIPPED = 2,
    R0FG1P_HIDDEN = 3,
    R0FG1P_INVALID_TIER = 255
};

void r0fg1_presentation_init(r0fg1_presentation *state);
uint8_t r0fg1_view_request(r0fg1_presentation *state, uint8_t view);
uint8_t r0fg1_presentation_bind(r0fg1_presentation *state,
                               const r0fg1_presentation_key *key,
                               int16_t horizon);
uint8_t r0fg1_anchor_add(r0fg1_presentation *state,
                        const r0fg1_presentation_key *key,
                        const r0fg1_anchor *anchor);
uint8_t r0fg1_occlusion_column(r0fg1_presentation *state,
                              const r0fg1_presentation_key *key,
                              uint8_t column, uint16_t ridge_y,
                              uint16_t ridge_depth);
// visible_bottom is changed only for an unclipped/clipped visible fragment.
uint8_t r0fg1_occlusion_clip(const r0fg1_presentation *state,
                            const r0fg1_presentation_key *key, uint8_t column,
                            uint16_t depth, uint16_t top, uint16_t bottom,
                            uint16_t *visible_bottom);
uint8_t r0fg1_presentation_complete(r0fg1_presentation *state,
                                   const r0fg1_presentation_key *key,
                                   uint8_t buffer_complete);
uint8_t r0fg1_presentation_swap(r0fg1_presentation *state);
void r0fg1_presentation_cancel(r0fg1_presentation *state);
uint8_t r0fg1_lod_select(uint8_t previous_tier, uint16_t pixels);

#endif
