// Independent comparison with the exact pre-change formatter compiled separately.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "m2_rebuild.h"

void reference_text_row(M2RebuildRenderer *renderer, uint8_t row);
void reference_glyph(char character, uint8_t pixels[64]);

int main(void)
{
    uint32_t state = 0x928113u;
    for (uint16_t test = 0u; test < 128u; ++test)
    {
        M2RebuildRenderer actual = {0};
        state = state * 1664525u + 1013904223u;
        actual.snapshot.tick = state;
        actual.snapshot.commands = ~state;
        actual.snapshot.fault = (uint8_t)state;
        actual.generation = state ^ 0x80000000u;
        actual.rejected = ~state;
        actual.source_age_at_text = state;
        actual.prepared.camera.revision = ~state;
        actual.prepared.camera.position.v[0] = ((int32_t)test - 64) * 180L * M2_POSITION_SCALE + 15;
        actual.prepared.camera.position.v[1] = ((int32_t)test - 64) * 90L * M2_POSITION_SCALE - 15;
        actual.prepared.camera.position.v[2] = -(10L + test * 20L) * M2_POSITION_SCALE;
        actual.prepared.camera.yaw = (int16_t)(test * 2u);
        actual.prepared.camera.pitch = (int16_t)((int16_t)(test % 121u) - 60);
        actual.prepared.camera.roll = (int16_t)(-actual.prepared.camera.pitch);
        for (uint8_t row = 0u; row < 9u; ++row)
        {
            M2RebuildRenderer expected = actual;
            reference_text_row(&expected, row);
            m2rb_text_row(&actual, row);
            assert(memcmp(actual.text, expected.text, 40u) == 0);
        }
    }
    for (uint16_t character = 0u; character < 128u; ++character)
    {
        uint8_t actual[64];
        uint8_t expected[64];
        reference_glyph((char)character, expected);
        m2rb_glyph((char)character, actual);
        assert(memcmp(actual, expected, sizeof(actual)) == 0);
    }
    puts("TEXT PASS: 1152 exact rows; 128 exact glyph comparisons");
    return 0;
}
