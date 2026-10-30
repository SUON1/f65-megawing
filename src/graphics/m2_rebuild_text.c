// Graphics-owned decimal/hex telemetry, without ROM fonts or formatted I/O.
#include <string.h>

#include "m2_rebuild.h"

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

// Control bytes select numeric fields; all printable bytes are literal labels.
// This private recipe preserves the existing 40-column telemetry contract.
static uint32_t field(const M2RebuildRenderer *renderer, uint8_t id)
{
    const M2Camera *camera = &renderer->prepared.camera;
    switch (id)
    {
        case 1u: return renderer->snapshot.tick;
        case 2u: return renderer->snapshot.commands;
        case 3u: return renderer->generation;
        case 4u: return camera->revision;
        case 5u: return renderer->source_age_at_text;
        case 6u: return renderer->snapshot.fault;
        case 7u: return renderer->rejected;
        case 8u: return (uint32_t)(camera->position.v[0] / M2_POSITION_SCALE);
        case 9u: return (uint32_t)(camera->position.v[1] / M2_POSITION_SCALE);
        case 10u: return (uint32_t)(-camera->position.v[2] / M2_POSITION_SCALE);
        case 11u: return (uint32_t)camera->yaw;
        case 12u: return (uint32_t)camera->pitch;
        default: return (uint32_t)camera->roll;
    }
}

void m2rb_text_row(M2RebuildRenderer *renderer, uint8_t row)
{
    static const char *const recipes[8] = {
        "NON-FLIGHT DIAGNOSTIC M2 REBUILD",
        "TICK \001 CMD \002", "GEN \003 CAM \004",
        "AGE AT TEXT \005 F \006 REJ \007",
        "CAM N\010 E\011 H\012 FT", "YAW\013 PITCH\014 ROLL\015",
        "ALTITUDE: NOT IMPLEMENTED", "AIRSPEED: NOT IMPLEMENTED"
    };
    memset(renderer->text, ' ', 40u);
    if (row >= 8u)
    {
        return;
    }
    const char *recipe = recipes[row];
    uint8_t column = 0u;
    while (*recipe != '\0' && column < 40u)
    {
        uint8_t token = (uint8_t)*recipe++;
        if (token >= 32u)
        {
            renderer->text[column++] = (char)token;
        }
        else if (token < 8u)
        {
            column = hex(renderer->text, column, field(renderer, token),
                         token == 6u ? 2u : 8u);
        }
        else
        {
            uint8_t digits = token < 10u ? 5u : token == 10u ? 4u
                : token == 11u ? 3u : 2u;
            // All signed fields are within +/-12000. Interpret the defined
            // unsigned conversion without relying on an out-of-range cast.
            uint32_t raw = field(renderer, token);
            int32_t value = raw <= INT32_MAX ? (int32_t)raw
                : -(int32_t)(0u - raw);
            column = decimal(renderer->text, column, value, digits);
        }
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
