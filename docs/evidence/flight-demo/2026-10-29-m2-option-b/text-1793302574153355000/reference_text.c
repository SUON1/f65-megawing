// Graphics-owned decimal/hex telemetry, without ROM fonts or formatted I/O.
#include <string.h>

#include "m2_rebuild.h"

static uint8_t label(char text[40], uint8_t column, const char *value)
{
    while (*value != '\0' && column < 40u)
    {
        text[column++] = *value++;
    }
    return column;
}

static uint8_t hex(char text[40], uint8_t column, uint32_t value, uint8_t digits)
{
    static const char alphabet[] = "0123456789ABCDEF";
    for (uint8_t i = 0u; i < digits && column < 40u; ++i)
    {
        uint8_t shift = (uint8_t)((digits - i - 1u) * 4u);
        text[column++] = alphabet[(value >> shift) & 15u];
    }
    return column;
}

static uint8_t decimal(char text[40], uint8_t column, int32_t value,
                       uint8_t digits)
{
    if (column >= 40u || (uint16_t)column + digits + 1u > 40u)
    {
        return column;
    }
    text[column++] = value < 0 ? '-' : '+';
    // All diagnostic operands are within +/-12000; no INT32_MIN negation.
    uint32_t magnitude = (uint32_t)(value < 0 ? -value : value);
    for (uint8_t i = 0u; i < digits; ++i)
    {
        text[column + digits - i - 1u] = (char)('0' + magnitude % 10u);
        magnitude /= 10u;
    }
    return (uint8_t)(column + digits);
}

void m2rb_text_row(M2RebuildRenderer *renderer, uint8_t row)
{
    char *text = renderer->text;
    const M2Camera *camera = &renderer->prepared.camera;
    uint8_t column = 0u;
    memset(text, ' ', 40u);
    switch (row)
    {
        case 0u:
            (void)label(text, 0u, "NON-FLIGHT DIAGNOSTIC M2 REBUILD");
            break;
        case 1u:
            column = label(text, 0u, "TICK ");
            column = hex(text, column, renderer->snapshot.tick, 8u);
            column = label(text, column, " CMD ");
            (void)hex(text, column, renderer->snapshot.commands, 8u);
            break;
        case 2u:
            column = label(text, 0u, "GEN ");
            column = hex(text, column, renderer->generation, 8u);
            column = label(text, column, " CAM ");
            (void)hex(text, column, camera->revision, 8u);
            break;
        case 3u:
            column = label(text, 0u, "AGE AT TEXT ");
            column = hex(text, column, renderer->source_age_at_text, 8u);
            column = label(text, column, " F ");
            column = hex(text, column, renderer->snapshot.fault, 2u);
            column = label(text, column, " REJ ");
            (void)hex(text, column, renderer->rejected, 8u);
            break;
        case 4u:
            column = label(text, 0u, "CAM N");
            column = decimal(text, column, camera->position.v[0] / M2_POSITION_SCALE, 5u);
            column = label(text, column, " E");
            column = decimal(text, column, camera->position.v[1] / M2_POSITION_SCALE, 5u);
            column = label(text, column, " H");
            column = decimal(text, column, -camera->position.v[2] / M2_POSITION_SCALE, 4u);
            (void)label(text, column, " FT");
            break;
        case 5u:
            column = label(text, 0u, "YAW");
            column = decimal(text, column, camera->yaw, 3u);
            column = label(text, column, " PITCH");
            column = decimal(text, column, camera->pitch, 2u);
            column = label(text, column, " ROLL");
            (void)decimal(text, column, camera->roll, 2u);
            break;
        case 6u:
            (void)label(text, 0u, "ALTITUDE: NOT IMPLEMENTED");
            break;
        case 7u:
            (void)label(text, 0u, "AIRSPEED: NOT IMPLEMENTED");
            break;
        default:
            break;
    }
}

// Original 5x7 glyph definitions. The unused rows/columns remain opaque black.
void m2rb_glyph(char character, uint8_t pixels[64])
{
    static const char characters[] = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-:+/";
    static const uint8_t rows[][7] = {
        {0,0,0,0,0,0,0}, {14,17,19,21,25,17,14}, {4,12,4,4,4,4,14},
        {14,17,1,2,4,8,31}, {30,1,1,14,1,1,30}, {2,6,10,18,31,2,2},
        {31,16,16,30,1,1,30}, {14,16,16,30,17,17,14}, {31,1,2,4,8,8,8},
        {14,17,17,14,17,17,14}, {14,17,17,15,1,1,14},
        {14,17,17,31,17,17,17}, {30,17,17,30,17,17,30},
        {14,17,16,16,16,17,14}, {30,17,17,17,17,17,30},
        {31,16,16,30,16,16,31}, {31,16,16,30,16,16,16},
        {14,17,16,23,17,17,15}, {17,17,17,31,17,17,17},
        {14,4,4,4,4,4,14}, {7,2,2,2,18,18,12},
        {17,18,20,24,20,18,17}, {16,16,16,16,16,16,31},
        {17,27,21,21,17,17,17}, {17,25,25,21,19,19,17},
        {14,17,17,17,17,17,14}, {30,17,17,30,16,16,16},
        {14,17,17,17,21,18,13}, {30,17,17,30,20,18,17},
        {15,16,16,14,1,1,30}, {31,4,4,4,4,4,4},
        {17,17,17,17,17,17,14}, {17,17,17,17,17,10,4},
        {17,17,17,21,21,27,17}, {17,17,10,4,10,17,17},
        {17,17,10,4,4,4,4}, {31,1,2,4,8,16,31},
        {0,0,0,31,0,0,0}, {0,4,4,0,4,4,0}, {0,4,4,31,4,4,0},
        {1,2,2,4,8,8,16}
    };
    uint8_t glyph = 0u;
    for (uint8_t i = 0u; i < sizeof(characters) - 1u; ++i)
    {
        if (characters[i] == character)
        {
            glyph = i;
            break;
        }
    }
    memset(pixels, M2RB_BLACK, 64u);
    for (uint8_t y = 0u; y < 7u; ++y)
    {
        for (uint8_t x = 0u; x < 5u; ++x)
        {
            if ((rows[glyph][y] & (uint8_t)(16u >> x)) != 0u)
            {
                pixels[y * 8u + x + 1u] = M2RB_WHITE;
            }
        }
    }
}
