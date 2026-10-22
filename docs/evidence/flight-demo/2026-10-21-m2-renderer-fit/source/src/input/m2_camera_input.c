#include "m2_camera_input.h"

uint16_t m2_camera_pressed(uint16_t *previous, uint16_t down)
{
    uint16_t pressed = (uint16_t)(down & (uint16_t)~*previous);
    *previous = down;
    return pressed;
}
