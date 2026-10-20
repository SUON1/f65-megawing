#include <string.h>

#include "m1_graphics.h"

static void text(uint8_t *row, uint8_t column, const char *value)
{
    while (*value != '\0' && column < M1_COLUMNS)
    {
        uint8_t character = (uint8_t)*value++;
        row[column++] = character >= 'A' && character <= 'Z'
                        ? (uint8_t)(character & 31u) : character;
    }
}

static void hex(uint8_t *row, uint8_t column, uint32_t value)
{
    for (uint8_t i = 0u; i < 8u; ++i)
    {
        uint8_t digit = (uint8_t)((value >> (28u - 4u * i)) & 15u);
        row[column + i] = digit < 10u ? (uint8_t)('0' + digit)
                                     : (uint8_t)(1u + digit - 10u);
    }
}

uint8_t m1_render_begin(M1Graphics *graphics, const M1Snapshot *source)
{
    if (graphics->busy || source->tick <= graphics->displayed_tick)
    {
        return 0u;
    }
    graphics->source = *source;
    graphics->destination = (uint8_t)(graphics->displayed_store ^ 1u);
    graphics->row = 0u;
    graphics->busy = 1u;
    graphics->ready = 0u;
    return 1u;
}

void m1_render_row(const M1Graphics *graphics, uint8_t row[M1_COLUMNS])
{
    memset(row, graphics->row < M1_OVERLAY_ROWS ? 32 : 160, M1_COLUMNS);
    switch (graphics->row)
    {
        case 0u:
            text(row, 1u, "65AERO M1 - NON-FLIGHT DIAGNOSTIC");
            break;
        case 1u:
            text(row, 1u, "100 HZ LOGICAL / 21 STAGES - TIMING NOT PHYSICAL ACCEPTANCE");
            break;
        case 2u:
            text(row, 1u, "TICK AT FRAME START ");
            hex(row, 21u, graphics->sampled_tick);
            text(row, 36u, "DEBT MAX CIA COUNTS ");
            hex(row, 56u, graphics->sampled_debt);
            break;
        case 3u:
            text(row, 1u, "SOURCE TICK ");
            hex(row, 13u, graphics->source.tick);
            text(row, 28u, "COMMANDS ");
            hex(row, 37u, graphics->source.commands);
            text(row, 50u, "FAULT ");
            hex(row, 56u, graphics->source.fault);
            break;
        case 4u:
            text(row, 1u, "CHECKSUM ");
            hex(row, 10u, graphics->source.checksum);
            text(row, 28u, "DISPLAYED GEN ");
            hex(row, 42u, graphics->generation + 1u);
            break;
        case 5u:
            text(row, 1u, "PUBLISHED GEN ");
            hex(row, 15u, graphics->published);
            text(row, 36u, "SOURCE AGE AT FRAME START ");
            hex(row, 62u, graphics->sampled_tick - graphics->source.tick);
            break;
        case 6u:
            text(row, 1u, "ALTITUDE: NOT IMPLEMENTED");
            text(row, 46u, "AIRSPEED: NOT IMPLEMENTED");
            break;
        case 7u:
            text(row, 1u, "SPACE: SEMANTIC PRESS/HOLD/RELEASE - NO AIRCRAFT STATE");
            break;
        default:
            break;
    }
}

void m1_render_advance(M1Graphics *graphics)
{
    if (graphics->busy && !graphics->ready)
    {
        ++graphics->row;
        graphics->ready = graphics->row == M1_ROWS;
    }
}

uint8_t m1_render_commit(M1Graphics *graphics)
{
    if (!graphics->busy || !graphics->ready
        || graphics->source.tick <= graphics->displayed_tick)
    {
        return 0u;
    }
    graphics->displayed_tick = graphics->source.tick;
    graphics->displayed_store = graphics->destination;
    ++graphics->generation;
    graphics->busy = 0u;
    graphics->ready = 0u;
    return 1u;
}

void m1_render_cancel(M1Graphics *graphics)
{
    graphics->busy = 0u;
    graphics->ready = 0u;
}

uint8_t m1_render_colors(uint8_t row, uint8_t colors[M1_COLUMNS])
{
    if (row >= M1_ROWS)
    {
        return 0u;
    }
    uint8_t color = row < M1_OVERLAY_ROWS ? M1_OVERLAY_COLOR
                    : (row < M1_HORIZON_ROW ? M1_SKY_COLOR : M1_GROUND_COLOR);
    memset(colors, color, M1_COLUMNS);
    return 1u;
}
