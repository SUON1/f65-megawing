// Host-only model of the private math registers and their transaction protocol.
#include <assert.h>
#include <stdint.h>
#include <string.h>

#include "wide_math.h"

enum
{
    NORMAL,
    BUSY_ON_ENTRY,
    NEVER_READY,
    NESTED_CALL,
    INTERRUPT_FAULT,
    REENTRY_DURING_READ
};

static uint8_t operands[8];
static uint8_t writes;
static uint8_t reads;
static uint8_t output_count;
static uint8_t pending;
static uint8_t idle_checked;
static uint8_t failed;
static uint8_t delay;
static uint8_t mode;
static unsigned polls;
static unsigned transactions;

static uint32_t decode(const uint8_t *bytes)
{
    uint32_t value = 0u;
    for (uint8_t i = 4u; i != 0u; --i)
    {
        value = (value << 8u) | bytes[i - 1u];
    }
    return value;
}

uint8_t m1_platform_fault(void)
{
    return failed;
}

static void reject_nested_call(void)
{
    uint8_t out[8];
    uint8_t in[4] = {0};
    memset(out, 0xa5, sizeof(out));
    assert(!m2rb_math_product(out, in, in));
    for (uint8_t i = 0u; i < sizeof(out); ++i)
    {
        assert(out[i] == 0xa5u);
    }
}

uint8_t m2math_bus_read(uint16_t address)
{
    if (address == 0xd70fu)
    {
        ++polls;
        if (!pending)
        {
            assert(writes == 0u && !idle_checked);
            idle_checked = 1u;
            return mode == BUSY_ON_ENTRY ? 0x40u : 0u;
        }
        assert(writes == 8u && reads == 0u);
        if (mode == NEVER_READY)
        {
            return 0x80u;
        }
        if (delay)
        {
            --delay;
            return 0xc0u;
        }
        pending = 0u;
        failed = (uint8_t)(mode == INTERRUPT_FAULT);
        return 0u;
    }
    assert(writes == 8u && !pending);
    uint64_t left = decode(operands);
    uint64_t right = decode(operands + 4u);
    if (reads == 0u)
    {
        assert(address == 0xd769u || address == 0xd778u);
        output_count = address == 0xd769u ? 4u : 8u;
        if (mode == REENTRY_DURING_READ)
        {
            reject_nested_call();
        }
    }
    uint64_t result;
    if (output_count == 4u)
    {
        assert(right >= (1ULL << 31u) && address == 0xd769u + reads);
        result = (left << 24u) / right;
    }
    else
    {
        assert(address == 0xd778u + reads);
        result = left * right;
    }
    uint8_t byte = (uint8_t)(result >> (8u * reads));
    if (++reads == output_count)
    {
        reads = 0u;
        writes = 0u;
        idle_checked = 0u;
        ++transactions;
    }
    return byte;
}

void m2math_bus_write(uint16_t address, uint8_t value)
{
    assert(idle_checked && !pending && writes < 8u);
    uint8_t index = (uint8_t)(writes / 2u + 4u * (writes & 1u));
    assert(address == 0xd770u + index);
    operands[index] = value;
    if (++writes == 8u)
    {
        pending = 1u;
    }
    if (mode == NESTED_CALL && writes == 4u)
    {
        reject_nested_call();
    }
}

unsigned m2math_transactions(void)
{
    return transactions;
}

#ifdef M2_MATH_SELF_TEST
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    assert(argc == 2);
    mode = (uint8_t)atoi(argv[1]);
    assert(mode <= REENTRY_DURING_READ);
    uint8_t left[4] = {0xffu, 0xffu, 0xffu, 0xffu};
    uint8_t right[4] = {1u, 0u, 0u, 0u};
    uint8_t output[8];
    memset(output, 0xa5, sizeof(output));
    assert(!m2rb_math_q24(output, left, right) && polls == 0u);
    if (mode == NORMAL)
    {
        delay = 7u;
        assert(m2rb_math_product(output, left, right));
        assert(polls == 9u && transactions == 1u && decode(output) == UINT32_MAX);
        assert(decode(output + 4u) == 0u);
        right[3] = 128u;
        assert(m2rb_math_q24(output, left, right));
        assert(transactions == 2u && decode(output) == 33554431u);
    }
    else
    {
        assert(!m2rb_math_product(output, left, right));
        assert(polls == (mode == BUSY_ON_ENTRY ? 1u : (mode == NEVER_READY ? 9u : 2u)));
        unsigned last = polls;
        assert(!m2rb_math_product(output, left, right) && polls == last);
        assert(!m2rb_math_product(output, left, right) && polls == last);
        for (uint8_t i = 0u; i < sizeof(output); ++i)
        {
            assert(output[i] == 0xa5u);
        }
    }
    printf("MATH GATEWAY PASS mode=%u polls=%u transactions=%u\n",
           (unsigned)mode, polls, transactions);
    return 0;
}
#endif
