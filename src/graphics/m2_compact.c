// One checked command interpreter for exact private numerical continuations.
#include <string.h>

#include "m2_compact.h"
#include "m2_fixture.h"
#include "m2_commands.inc"

static const uint8_t entries[3] = {M2P_PREPARE,M2P_PROJECT,M2P_HORIZON};
static const uint8_t ends[3] = {M2P_PREPARE_END,M2P_PROJECT_END,M2P_HORIZON_END};

static void sine(M2Wide out, int16_t angle)
{
    int16_t wrapped = (int16_t)(angle % 360);
    if (wrapped < 0)
    {
        wrapped += 360;
    }
    uint8_t negative = (uint8_t)(wrapped > 180);
    if (negative)
    {
        wrapped -= 180;
    }
    if (wrapped > 90)
    {
        wrapped = (int16_t)(180 - wrapped);
    }
    memcpy(out, &m2_sine_q46[(uint16_t)wrapped], 8u);
    if (negative)
    {
        m2w_negate(out, 8u);
    }
}


static void start(M2Compact *work, uint8_t kind)
{
    work->kind = kind;
    work->state = entries[kind];
    work->waiting = 0u;
    work->bound = 0u;
    work->product_ready = 0u;
    work->return_active = 0u;
    work->job.phase = 0u;
    memset(work->counters, 0, sizeof(work->counters));
}

static uint8_t jump(M2Compact *work, uint8_t target)
{
    if (target < entries[work->kind] || target >= ends[work->kind])
    {
        return 0u;
    }
    work->state = target;
    return 1u;
}

static void bind(M2Compact *work, struct M2Prepared *prepared, M2Horizon *horizon)
{
    for (uint8_t i = 0u; i < 10u; ++i)
    {
        work->ports[i] = work->registers[i];
    }
    work->ports[10] = work->sum;
    work->ports[11] = work->temporary;
    work->ports[12] = work->job.value;
    for (uint8_t i = 0u; i < 9u; ++i)
    {
        work->ports[13u + i] = (uint8_t *)&prepared->rotation.m[i];
    }
    for (uint8_t i = 0u; i < 3u; ++i)
    {
        work->ports[22u + i] = horizon == 0 ? 0 : (uint8_t *)horizon + i * 8u;
    }
    work->bound = 1u;
}

static uint8_t *operand(M2Compact *work, uint8_t selector, uint8_t write)
{
    if (selector >= 128u)
    {
        uint8_t index = (uint8_t)(selector - 128u);
        if (write || index >= sizeof(m2_command_constants) / sizeof(m2_command_constants[0]))
        {
            return 0;
        }
        return (uint8_t *)&m2_command_constants[index];
    }
    uint8_t end = work->counters[0];
    uint8_t row = work->counters[1];
    uint8_t axis = work->counters[2];
    if (selector == 25u)
    {
        selector = (uint8_t)(13u + row * 3u + axis);
    }
    else if (selector == 26u)
    {
        selector = (uint8_t)(end * 3u + row);
    }
    else if (selector == 27u || selector == 28u)
    {
        if (!work->return_active || (work->outside != 0u && work->outside != 3u)
            || work->inside != (uint8_t)(work->outside ^ 3u))
        {
            return 0;
        }
        selector = (uint8_t)((selector == 27u ? work->outside : work->inside) + axis);
    }
    else if (selector == 29u)
    {
        if (axis >= 2u)
        {
            return 0;
        }
        selector = (uint8_t)(end * 3u + axis + 1u);
    }
    else if (selector == 30u)
    {
        selector = (uint8_t)(end * 3u);
    }
    return selector < 25u ? work->ports[selector] : 0;
}

// One instruction or arithmetic kernel unit. No caller-owned snapshot is held.
static int8_t m2_command_service(M2Compact *work, struct M2Prepared *prepared,
                        M2Horizon *horizon, M2Line *line)
{
    if (work->kind >= 3u || prepared == 0
        || work->state < entries[work->kind] || work->state >= ends[work->kind]
        || work->counters[0] >= 2u || work->counters[1] >= 3u || work->counters[2] >= 3u)
    {
        return -1;
    }
    if (!work->bound)
    {
        bind(work, prepared, horizon);
    }
    else if (work->ports[0] != work->registers[0]
        || work->ports[13] != (uint8_t *)&prepared->rotation.m[0]
        || work->ports[22] != (horizon == 0 ? 0 : (uint8_t *)horizon))
    {
        return -1;
    }
    const uint8_t *command = m2_commands[work->state];
    uint8_t opcode = command[0];
    uint8_t operation = (uint8_t)(opcode & 31u);
    uint8_t *destination = opcode & 32u ? operand(work, command[1], 1u) : 0;
    uint8_t *first = opcode & 64u ? operand(work, command[2], 0u) : 0;
    uint8_t *last = opcode & 128u ? operand(work, command[3], 0u) : 0;
    if (((opcode & 32u) && destination == 0)
        || ((opcode & 64u) && first == 0) || ((opcode & 128u) && last == 0))
    {
        return -1;
    }
    if (operation >= 8u && operation <= 14u)
    {
        uint8_t flags = operation == 11u ? 192u : (operation == 13u ? 160u : 224u);
        if (opcode != (uint8_t)(flags | operation))
        {
            return -1;
        }
        if (!work->waiting)
        {
            uint8_t ok;
            if (operation >= 13u)
            {
                if (!work->product_ready)
                {
                    return -1;
                }
                ok = m2l_divide(&work->job, last);
            }
            else
            {
                uint8_t shift = operation == 11u ? 255u : (operation == 12u ? 0u : 46u);
                ok = m2l_multiply(&work->job, first, last, shift);
            }
            work->product_ready = 0u;
            if (!ok)
            {
                return -1;
            }
            work->waiting = 1u;
            return 0;
        }
        if (work->job.phase != (operation >= 13u ? 2u : 1u))
        {
            return -1;
        }
        int8_t result = m2l_service(&work->job);
        if (result <= 0)
        {
            return result;
        }
        work->waiting = 0u;
        if (operation == 11u)
        {
            work->product_ready = 1u;
        }
        else if (operation == 9u || operation == 10u || operation == 12u || operation == 14u)
        {
            m2w_add(destination, operation == 14u ? first : destination,
                      work->job.value, (uint8_t)(operation == 10u));
        }
        else
        {
            memcpy(destination, work->job.value, 8u);
        }
        ++work->state;
        return 0;
    }
    switch (opcode)
    {
        case M2V_COPY:
            memcpy(destination, first, 8u);
            break;
        case M2V_ADD:
        case M2V_SUB:
            m2w_add(destination, first, last, (uint8_t)(opcode == M2V_SUB));
            break;
        case M2V_NEG:
            memcpy(destination, first, 8u);
            m2w_negate(destination, 8u);
            break;
        case M2V_DOUBLE:
            m2w_double(destination);
            break;
        case M2V_SINE:
        {
            if (command[2] > 2u || (command[3] != 0u && command[3] != 90u))
            {
                return -1;
            }
            int16_t angle = command[2] == 0u ? prepared->camera.yaw
                : (command[2] == 1u ? prepared->camera.pitch : prepared->camera.roll);
            sine(destination, (int16_t)(angle + command[3]));
            break;
        }
        case M2V_DELTA:
        {
            uint8_t axis = work->counters[2];
            int32_t delta = work->endpoints[work->counters[0]].v[axis]
                - prepared->camera.position.v[axis];
            m2w_i32(destination, delta);
            for (uint8_t bit = 0u; bit < 12u; ++bit)
            {
                m2w_double(destination);
            }
            break;
        }
        case M2V_NEXT:
        {
            if (command[1] >= 3u || command[2] == 0u || command[2] > 3u
                || work->counters[command[1]] >= command[2])
            {
                return -1;
            }
            if (++work->counters[command[1]] < command[2])
            {
                return jump(work, command[3]) ? 0 : -1;
            }
            work->counters[command[1]] = 0u;
            break;
        }
        case M2V_JUMP:
            return jump(work, command[2]) ? 0 : -1;
        case M2V_CLIP:
        {
            uint8_t first_negative = (uint8_t)(work->registers[6][7] >> 7u);
            uint8_t last_negative = (uint8_t)(work->registers[7][7] >> 7u);
            if (first_negative && last_negative)
            {
                work->state = 255u;
                return 2;
            }
            if (first_negative != last_negative)
            {
                if (work->return_active)
                {
                    return -1;
                }
                work->outside = first_negative ? 0u : 3u;
                work->inside = first_negative ? 3u : 0u;
                memcpy(work->registers[8], work->registers[first_negative ? 7u : 6u], 8u);
                m2w_add(work->registers[9], work->registers[8],
                          work->registers[first_negative ? 6u : 7u], 1u);
                work->counters[2] = 0u;
                work->return_pc = (uint8_t)(work->state + 1u);
                work->return_active = 1u;
                return jump(work, command[2]) ? 0 : -1;
            }
            break;
        }
        case M2V_RETURN:
            if (!work->return_active)
            {
                return -1;
            }
            work->return_active = 0u;
            return jump(work, work->return_pc) ? 0 : -1;
        case M2V_SCREEN:
        {
            uint8_t axis = work->counters[2];
            int32_t value;
            if (axis >= 2u || !m2w_narrow(work->temporary, &value))
            {
                return -1;
            }
            int32_t extent = axis == 0u ? M2_WIDTH : M2_HEIGHT;
            value += (extent - 1) * (M2_SCREEN_SCALE / 2);
            int32_t maximum = extent * M2_SCREEN_SCALE - M2_SCREEN_SCALE / 2;
            if (value < -M2_SCREEN_SCALE / 2)
            {
                value = -M2_SCREEN_SCALE / 2;
            }
            if (value > maximum)
            {
                value = maximum;
            }
            if (axis == 0u)
            {
                work->line.x[work->counters[0]] = value;
            }
            else
            {
                work->line.y[work->counters[0]] = value;
            }
            break;
        }
        case M2V_HORIZON_INIT:
            if (horizon == 0)
            {
                return -1;
            }
            horizon->positive = (uint8_t)((((const uint8_t *)&prepared->rotation.m[5])[7] & 128u) == 0u);
            horizon->cursor = horizon->positive ? 320u : 0u;
            horizon->row = 0u;
            break;
        case M2V_HORIZON_STEP:
        {
            if (horizon == 0 || horizon->row >= 128u || horizon->cursor > 320u)
            {
                return -1;
            }
            uint8_t can_advance = horizon->positive ? horizon->cursor != 0u : horizon->cursor != 320u;
            if (can_advance && m2w_positive(horizon->edge))
            {
                if (horizon->positive)
                {
                    --horizon->cursor;
                }
                else
                {
                    ++horizon->cursor;
                }
                m2w_add(horizon->edge, horizon->edge, horizon->dx, horizon->positive);
                return 0;
            }
            horizon->boundary[horizon->row] = horizon->cursor;
            if (++horizon->row < 128u)
            {
                m2w_add(horizon->edge, horizon->edge, horizon->dy, 0u);
                return 0;
            }
            break;
        }
        case M2V_DONE:
            if (command[1] != work->kind + 1u)
            {
                return -1;
            }
            if (work->kind == 0u)
            {
                prepared->ready = 1u;
            }
            else if (work->kind == 1u)
            {
                if (line == 0)
                {
                    return -1;
                }
                *line = work->line;
            }
            else
            {
                horizon->state = 2u;
            }
            work->state = 255u;
            return 1;
        case M2V_NEGATIVE:
            if (first[7] & 128u)
            {
                return jump(work, command[3]) ? 0 : -1;
            }
            break;
        case M2V_POSITIVE:
            if (!m2w_positive(first))
            {
                return -1;
            }
            break;
        default:
            return -1;
    }
    ++work->state;
    return 0;
}

void m2c_prepare_begin(M2Compact *work)
{
    start(work, 0u);
}

int8_t m2c_prepare_service(M2Compact *work, struct M2Prepared *prepared)
{
    return work->kind == 0u ? m2_command_service(work, prepared, 0, 0) : -1;
}

uint8_t m2c_project_begin(M2Compact *work, const M2Point *first, const M2Point *last)
{
    if (!m2_point_valid(first) || !m2_point_valid(last))
    {
        return 0u;
    }
    work->endpoints[0] = *first;
    work->endpoints[1] = *last;
    start(work, 1u);
    return 1u;
}

int8_t m2c_project_service(M2Compact *work, const struct M2Prepared *prepared,
                            M2Line *line)
{
    if (work->kind != 1u || prepared == 0 || prepared->ready != 1u || line == 0)
    {
        return -1;
    }
    // Project instructions only read the captured transform.
    return m2_command_service(work, (struct M2Prepared *)prepared, 0, line);
}

void m2c_horizon_begin(M2Horizon *horizon)
{
    horizon->state = 0u;
}

int8_t m2c_horizon_service(M2Horizon *horizon, M2Compact *work,
                            const struct M2Prepared *prepared)
{
    if (prepared == 0 || prepared->ready != 1u || horizon->state > 1u)
    {
        return -1;
    }
    if (horizon->state == 0u)
    {
        start(work, 2u);
        horizon->state = 1u;
    }
    if (work->kind != 2u)
    {
        return -1;
    }
    return m2_command_service(work, (struct M2Prepared *)prepared, horizon, 0);
}
