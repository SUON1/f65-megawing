// Graphics-owned diagnostic labels and direct field composition; no ROM font.
#include <stddef.h>
#include <string.h>

#include "m2_rebuild.h"

enum { HEX32, HEX8, POSITION, HEIGHT, ANGLE };

typedef struct
{
    uint16_t offset;
    uint8_t row;
    uint8_t column;
    uint8_t kind;
    uint8_t digits;
} TextField;

static const TextField fields[] = {
    {offsetof(M2RebuildRenderer, snapshot.tick), 1,5,HEX32,8},
    {offsetof(M2RebuildRenderer, snapshot.commands), 1,18,HEX32,8},
    {offsetof(M2RebuildRenderer, generation), 2,4,HEX32,8},
    {offsetof(M2RebuildRenderer, prepared.camera.revision), 2,17,HEX32,8},
    {offsetof(M2RebuildRenderer, source_age_at_text), 3,12,HEX32,8},
    {offsetof(M2RebuildRenderer, snapshot.fault), 3,23,HEX8,2},
    {offsetof(M2RebuildRenderer, rejected), 3,30,HEX32,8},
    {offsetof(M2RebuildRenderer, prepared.camera.position.v[0]), 4,5,POSITION,5},
    {offsetof(M2RebuildRenderer, prepared.camera.position.v[1]), 4,13,POSITION,5},
    {offsetof(M2RebuildRenderer, prepared.camera.position.v[2]), 4,21,HEIGHT,4},
    {offsetof(M2RebuildRenderer, prepared.camera.yaw), 5,3,ANGLE,3},
    {offsetof(M2RebuildRenderer, prepared.camera.pitch), 5,13,ANGLE,2},
    {offsetof(M2RebuildRenderer, prepared.camera.roll), 5,21,ANGLE,2}
};

static void number(char *text, const uint8_t *source, uint8_t kind, uint8_t digits)
{
    uint32_t magnitude = 0u;
    if (kind == ANGLE)
    {
        int16_t angle;
        memcpy(&angle, source, sizeof(angle));
        magnitude = (uint32_t)(int32_t)angle;
    }
    else
    {
        memcpy(&magnitude, source, kind == HEX8 ? 1u : 4u);
    }
    if (kind >= POSITION)
    {
        int32_t value;
        memcpy(&value, &magnitude, sizeof(value));
        if (kind != ANGLE)
        {
            value /= M2_POSITION_SCALE;
        }
        if (kind == HEIGHT)
        {
            value = -value;
        }
        *text++ = value < 0 ? '-' : '+';
        magnitude = (uint32_t)(value < 0 ? -value : value);
    }
    static const char alphabet[] = "0123456789ABCDEF";
    for (uint8_t i = digits; i != 0u; --i)
    {
        uint8_t digit;
        if (kind < POSITION)
        {
            digit = (uint8_t)(magnitude & 15u);
            magnitude >>= 4u;
        }
        else
        {
            digit = (uint8_t)(magnitude % 10u);
            magnitude /= 10u;
        }
        text[i - 1u] = alphabet[digit];
    }
}

void m2rb_text_row(M2RebuildRenderer *renderer, uint8_t row)
{
    static const char *const templates[8] = {
        "NON-FLIGHT DIAGNOSTIC M2 UNBANKED",
        "TICK          CMD         ",
        "GEN          CAM         ",
        "AGE AT TEXT          F    REJ         ",
        "CAM N       E       H      FT",
        "YAW     PITCH    ROLL    ",
        "ALTITUDE: NOT IMPLEMENTED",
        "               AIRSPEED: NOT IMPLEMENTED"
    };
    memset(renderer->text, ' ', 40u);
    if (row >= 8u)
    {
        return;
    }
    const char *label = templates[row];
    for (uint8_t column = 0u; column < 40u && label[column] != '\0'; ++column)
    {
        renderer->text[column] = label[column];
    }
    for (uint8_t i = 0u; i < sizeof(fields) / sizeof(fields[0]); ++i)
    {
        if (fields[i].row == row)
        {
            number(&renderer->text[fields[i].column],
                     (const uint8_t *)renderer + fields[i].offset,
                     fields[i].kind, fields[i].digits);
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
