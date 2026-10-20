// Graphics binds one immutable snapshot until a complete world is committed.
#pragma once
#include "m1_snapshot.h"

// Scene policy belongs to Graphics, including initialization color rows.
enum
{
    M1_OVERLAY_ROWS = 9,
    M1_HORIZON_ROW = 13,
    M1_SCENE_BACKGROUND = 0,
    M1_SCENE_BORDER = 0,
    M1_OVERLAY_COLOR = 1,
    M1_SKY_COLOR = 6,
    M1_GROUND_COLOR = 5
};

typedef struct
{
    M1Snapshot source;
    uint32_t sampled_tick;
    uint32_t sampled_debt;
    uint32_t published;
    uint32_t displayed_tick;
    uint32_t generation;
    uint8_t row;
    uint8_t busy;
    uint8_t ready;
    uint8_t destination;
    uint8_t displayed_store;
} M1Graphics;

uint8_t m1_render_begin(M1Graphics *graphics, const M1Snapshot *source);
void m1_render_row(const M1Graphics *graphics, uint8_t row[M1_COLUMNS]);
void m1_render_advance(M1Graphics *graphics);
uint8_t m1_render_commit(M1Graphics *graphics);
void m1_render_cancel(M1Graphics *graphics);
uint8_t m1_render_colors(uint8_t row, uint8_t colors[M1_COLUMNS]);
