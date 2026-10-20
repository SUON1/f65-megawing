#pragma once
#include "m1_runtime.h"

typedef struct
{
    uint8_t previous;
} M1Input;

uint8_t m1_input_sample(M1Input *input, M1Core *core, uint8_t down);
