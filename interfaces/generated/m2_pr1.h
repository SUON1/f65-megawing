// Generated M2 PR1 development records; not a production ABI.
#pragma once
#include <stdint.h>
// Source SHA256: 4832867688dc11c98cf816ae00254778f82a69dfb2b13af0e63d5db7ce36cda6
#define M2_FIXTURE_REVISION (1L)
#define M2_PROJECTION_REVISION (2L)
#define M2_COMPOSITION_REVISION (1L)
#define M2_WIDTH (320L)
#define M2_HEIGHT (128L)
#define M2_FOCAL (160L)
#define M2_POSITION_SCALE (4096L)
#define M2_ROTATION_SCALE (70368744177664LL)
#define M2_SCREEN_SCALE (65536L)
#define M2_NEAR_FT (10L)
#define M2_FAR_FT (40000L)
#define M2_WORLD_LIMIT_FT (65536L)
#define M2_NORTH_LIMIT_FT (12000L)
#define M2_EAST_LIMIT_FT (6000L)
#define M2_HEIGHT_MIN_FT (10L)
#define M2_HEIGHT_MAX_FT (3000L)
#define M2_TILT_LIMIT_DEG (60L)
#define M2_RUNWAY_HALF_LENGTH_FT (3000L)
#define M2_RUNWAY_HALF_WIDTH_FT (75L)
#define M2_THRESHOLD_NORTH_FT (2900L)
#define M2_MARK_FIRST_FT (-2500L)
#define M2_MARK_LAST_FT (2500L)
#define M2_MARK_STEP_FT (500L)
#define M2_MARK_HALF_LENGTH_FT (50L)
#define M2_SEGMENT_COUNT (17L)
#define M2_CLIP_PLANES (6L)
#define M2_RASTER_POINTS (320L)
#define M2_CLIP_SCALE (16777216L)
#define M2_VERTICAL_NUM (2L)
#define M2_VERTICAL_DEN (5L)
typedef struct
{
    int32_t v[3];
} M2Point;
typedef struct
{
    M2Point position;
    int16_t yaw;
    int16_t pitch;
    int16_t roll;
    uint32_t revision;
} M2Camera;
typedef struct
{
    int64_t m[9];
} M2Transform;
typedef struct
{
    int32_t x[2];
    int32_t y[2];
} M2Line;
typedef struct
{
    uint16_t x;
    uint16_t y;
} M2Pixel;
typedef struct
{
    uint32_t fixture_revision;
    int32_t down;
    uint8_t inside;
} M2Surface;
typedef struct
{
    M2Camera camera;
    M2Transform transform;
    uint32_t generation;
    uint32_t source_tick;
    uint32_t fixture_revision;
    uint32_t projection_revision;
    uint32_t composition_revision;
    uint16_t view_id;
    uint16_t tier_id;
    uint8_t store;
} M2Registration;
extern const int64_t m2_sine_q46[91];
