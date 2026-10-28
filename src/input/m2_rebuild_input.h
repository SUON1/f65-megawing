// Input-owned semantic edge state; diagnostic camera input never enters physics.
#pragma once
#include <stdint.h>

enum
{
    M2RB_NORTH = 1u, M2RB_SOUTH = 2u, M2RB_EAST = 4u, M2RB_WEST = 8u,
    M2RB_UP = 16u, M2RB_DOWN = 32u, M2RB_YAW_LEFT = 64u,
    M2RB_YAW_RIGHT = 128u, M2RB_PITCH_UP = 256u, M2RB_PITCH_DOWN = 512u,
    M2RB_ROLL_LEFT = 1024u, M2RB_ROLL_RIGHT = 2048u, M2RB_RESET = 4096u
};

typedef struct
{
    uint16_t previous;
} M2RebuildInput;

uint16_t m2rb_input_edges(M2RebuildInput *input, uint16_t down);
