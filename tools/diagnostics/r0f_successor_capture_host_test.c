#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "r0f_successor_integration.h"
#include "successor_capture.h"

static uint8_t record[512];
volatile uint8_t *const cfresult = record;
static uint8_t seen[512];
static uint8_t current_page;
static unsigned calls;

void cfscreen(void)
{
    calls++;
}

void cfline(uint8_t row, const char *text)
{
    assert(row < 25u);
    assert(strlen(text) <= 80u);
    calls++;
}

uint32_t cfget32(uint16_t offset)
{
    assert(offset == R0FSI_O_CRC32);
    return 0x12345678u;
}

void cfhex(uint8_t row, uint8_t column, uint32_t value, uint8_t digits)
{
    calls++;
    assert(row < 25u && column + digits <= 80u);
    if (row == 3u)
    {
        assert((column == 5u && value == current_page + 1u && digits == 2u)
               || (column == 22u && value == 0x12345678u && digits == 8u));
        return;
    }
    assert(row >= 5u && row < 21u);
    unsigned offset = current_page * 256u + (row - 5u) * 16u;
    if (column == 0u)
    {
        assert(digits == 4u && value == offset);
        return;
    }
    assert(column >= 6u && (column - 6u) % 3u == 0u);
    offset += (column - 6u) / 3u;
    assert(offset < 512u && digits == 2u && value == record[offset]);
    seen[offset]++;
}

int main(void)
{
    for (unsigned index = 0u; index < 512u; index++)
    {
        record[index] = (uint8_t)(index ^ (index >> 8u));
    }
    uint8_t before[512];
    memcpy(before, record, sizeof(record));
    for (current_page = 0u; current_page < 2u; current_page++)
    {
        r0fsi_capture_page(current_page);
    }
    for (unsigned index = 0u; index < 512u; index++)
    {
        assert(seen[index] == 1u);
    }
    assert(memcmp(before, record, sizeof(record)) == 0);
    unsigned previous_calls = calls;
    for (unsigned page = 2u; page < 256u; page++)
    {
        r0fsi_capture_page((uint8_t)page);
    }
    assert(calls == previous_calls);
    puts("PASS: 512 bytes, two pages, 254 invalid pages, immutable result");
    return 0;
}
