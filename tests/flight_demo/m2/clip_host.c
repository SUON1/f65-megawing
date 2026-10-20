// Execute the independent regression vectors with ASan/UBSan, host only.
#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "m2_geometry.h"

typedef struct
{
    M2Camera camera;
    M2Point first;
    M2Point last;
    M2Line expected;
    int8_t visible;
} ClipCase;

#include "clip_vectors.h"

int main(void)
{
    for (size_t i = 0u; i < sizeof(clip_cases) / sizeof(clip_cases[0]); ++i)
    {
        const ClipCase *test = &clip_cases[i];
        M2Line line;
        memset(&line, 0x55, sizeof(line));
        M2Line unchanged = line;
        int8_t status = m2_project_segment(&test->camera, &test->first,
                                            &test->last, &line);
        assert(status == test->visible);
        if (status == 0)
        {
            assert(memcmp(&line, &unchanged, sizeof(line)) == 0);
            continue;
        }
        for (uint8_t end = 0u; end < 2u; ++end)
        {
            int32_t dx = line.x[end] - test->expected.x[end];
            int32_t dy = line.y[end] - test->expected.y[end];
            // Half pixel plus one Q16 unit for reference serialization rounding.
            assert(dx >= -32769 && dx <= 32769);
            assert(dy >= -32769 && dy <= 32769);
        }
    }
    puts("M2 CLIPPING SANITIZERS PASS: 841 near/far/reversed regression cases");
    return 0;
}
