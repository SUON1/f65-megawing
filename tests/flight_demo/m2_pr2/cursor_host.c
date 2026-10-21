// Cursor lifecycle and bounded-work checks; geometric correctness is checked
// separately by the unchanged independent Decimal/raster oracle.
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "m2_geometry.h"
#include "m2_raster_private.h"

int main(void)
{
    M2Line line = {{0, 3 * M2_SCREEN_SCALE}, {0, 2 * M2_SCREEN_SCALE}};
    const M2Pixel expected[] = {{0, 0}, {1, 1}, {2, 1}, {3, 2}};
    struct M2RasterCursor first = {0};
    struct M2RasterCursor second = {0};
    M2Pixel pixel = {99, 99};
    assert(!m2_raster_next(&first, &pixel));
    assert(pixel.x == 99 && pixel.y == 99);
    assert(m2_raster_begin(&line, &first));
    assert(m2_raster_begin(&line, &second));
    for (uint16_t index = 0u; index < 4u; ++index)
    {
        struct M2RasterCursor saved = first;
        assert(!m2_raster_next(&first, 0));
        assert(memcmp(&first, &saved, sizeof(first)) == 0);
        assert(m2_raster_next(&first, &pixel));
        assert(pixel.x == expected[index].x && pixel.y == expected[index].y);
        // An unrelated continuation can progress without corrupting this one.
        assert(m2_raster_next(&second, &pixel));
        assert(pixel.x == expected[index].x && pixel.y == expected[index].y);
        assert(first.remaining == 3u - index);
    }
    assert(!m2_raster_next(&first, &pixel));
    assert(pixel.x == 3 && pixel.y == 2);
    struct M2RasterCursor saved = first;
    M2Line invalid = line;
    invalid.x[0] = -M2_SCREEN_SCALE;
    assert(!m2_raster_begin(&invalid, &first));
    assert(memcmp(&first, &saved, sizeof(first)) == 0);
    assert(!m2_raster_begin(0, &first));
    assert(!m2_raster_begin(&line, 0));
    assert(!m2_raster_next(0, &pixel));
    // Restart after partial consumption; old work has no hidden shared state.
    assert(m2_raster_begin(&line, &first));
    assert(m2_raster_next(&first, &pixel));
    M2Line point = {{7 * M2_SCREEN_SCALE, 7 * M2_SCREEN_SCALE},
                    {9 * M2_SCREEN_SCALE, 9 * M2_SCREEN_SCALE}};
    assert(m2_raster_begin(&point, &first));
    assert(m2_raster_next(&first, &pixel));
    assert(pixel.x == 7 && pixel.y == 9 && first.remaining == 0);
    assert(!m2_raster_next(&first, &pixel));
    puts("PASS cursor pause/interleave/restart/exhaustion/null/invalid-output invariants");
    return 0;
}
