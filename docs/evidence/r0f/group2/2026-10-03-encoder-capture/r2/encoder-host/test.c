#include <assert.h>
#include <stdint.h>
#include <stdio.h>
static volatile uint8_t r0f_pf_copy_request[9];
static uint8_t result;
static unsigned calls;
static uint8_t r0f_pf_flat_copy(void) { calls++; return result; }
uint8_t r0fg2_copy(uint32_t source, uint32_t destination, uint8_t bytes)
{
    for (uint8_t index = 0u; index < 4u; index++)
    {
        r0f_pf_copy_request[index] = (uint8_t)(source >> (index * 8u));
        r0f_pf_copy_request[4u + index] = (uint8_t)(destination >> (index * 8u));
    }
    r0f_pf_copy_request[8] = bytes;
    return r0f_pf_flat_copy();
}

int main(void)
{
    const uint32_t addresses[] = {0,255,256,65535,65536,0xffffff,0x1000000,0xffffffff};
    unsigned cases = 0;
    for (unsigned a = 0; a < 8; a++)
    {
        for (unsigned b = 0; b < 8; b++)
        {
            for (unsigned n = 1; n <= 255; n += 254)
            {
                for (result = 0; result < 2; result++)
                {
                    unsigned before = calls;
                    assert(r0fg2_copy(addresses[a], addresses[b], n) == result);
                    assert(calls == before + 1);
                    uint32_t source = 0, destination = 0;
                    for (int i = 3; i >= 0; i--)
                    {
                        source = source * 256 + r0f_pf_copy_request[i];
                        destination = destination * 256 + r0f_pf_copy_request[4+i];
                    }
                    assert(source == addresses[a] && destination == addresses[b]);
                    assert(r0f_pf_copy_request[8] == n);
                    cases++;
                }
            }
        }
    }
    printf("PASS: %u exact nine-byte requests, carry boundaries and both PF returns\n", cases);
}
