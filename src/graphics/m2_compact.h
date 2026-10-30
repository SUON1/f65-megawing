// Graphics-owned arithmetic continuation. Never serialized or shared with Core.
#pragma once
#include "m2_limb.h"
#include "m2_prepared_private.h"

// Deliberate specialization of the approved profile, never silent drift.
_Static_assert(M2_CLIP_SCALE == (1L << 24u), "Q24 contract changed");
_Static_assert(M2_CLIP_SCALE / M2_POSITION_SCALE == (1L << 12u), "position ratio changed");
_Static_assert(M2_ROTATION_SCALE == (1LL << 46u), "Q46 contract changed");
_Static_assert(M2_SCREEN_SCALE == (1L << 16u), "Q16 contract changed");
_Static_assert(M2_VERTICAL_NUM == 2 && M2_VERTICAL_DEN == 5, "clip planes changed");
_Static_assert(M2_WIDTH == 320 && M2_HEIGHT == 128 && M2_FOCAL == 160, "projection changed");
_Static_assert(M2_WORLD_LIMIT_FT == 65536 && M2_NORTH_LIMIT_FT == 12000
    && M2_EAST_LIMIT_FT == 6000 && M2_HEIGHT_MAX_FT == 3000
    && M2_HEIGHT_MIN_FT == 10 && M2_TILT_LIMIT_DEG == 60
    && M2_NEAR_FT == 10 && M2_FAR_FT == 40000, "numeric envelope changed");
_Static_assert(sizeof(int64_t) == 8, "eight-byte public wide records required");
#if __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
#error "Private wide byte adapters require little endian"
#endif

typedef struct
{
    M2LimbJob job;
    M2Wide registers[10];
    M2Wide sum;
    M2Wide temporary;
    M2Point endpoints[2];
    M2Line line;
    uint8_t state;
    uint8_t index;
    uint8_t endpoint;
    uint8_t row;
    uint8_t axis;
    uint8_t plane;
    uint8_t outside;
    uint8_t inside;
} M2Compact;

typedef struct
{
    M2Wide edge;
    M2Wide dx;
    M2Wide dy;
    uint16_t boundary[128];
    uint16_t cursor;
    uint8_t row;
    uint8_t positive;
    uint8_t state;
} M2Horizon;

void m2c_prepare_begin(M2Compact *work);
int8_t m2c_prepare_service(M2Compact *work, struct M2Prepared *prepared);
uint8_t m2c_project_begin(M2Compact *work, const M2Point *first, const M2Point *last);
// 0 continues, 1 visible, 2 empty, -1 invalid. Output only written when visible.
int8_t m2c_project_service(M2Compact *work, const struct M2Prepared *prepared,
                            M2Line *line);
void m2c_horizon_begin(M2Horizon *horizon);
int8_t m2c_horizon_service(M2Horizon *horizon, M2Compact *work,
                            const struct M2Prepared *prepared);
