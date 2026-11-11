// Host-only independent formatting expectations; never linked on target.
#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "m2_rebuild.h"

int main(void)
{
    M2RebuildRenderer renderer = {0};
    char expected[81];
    static const int32_t positions[] = {-12000,-1,0,1,12000};
    uint32_t comparisons = 0u;
    for (uint16_t sample = 0u; sample < 256u; ++sample)
    {
        renderer.snapshot.tick = 0x1020304u * sample;
        renderer.snapshot.commands = ~renderer.snapshot.tick;
        renderer.generation = renderer.snapshot.tick ^ 0xA5A5A5A5u;
        renderer.prepared.camera.revision = ~renderer.generation;
        renderer.source_age_at_text = renderer.snapshot.tick + 0x10203040u;
        renderer.snapshot.fault = (uint8_t)sample;
        renderer.rejected = renderer.snapshot.commands;
        renderer.prepared.camera.position.v[0] = positions[sample % 5u] * (int32_t)M2_POSITION_SCALE;
        renderer.prepared.camera.position.v[1] = positions[(sample + 1u) % 5u] * (int32_t)M2_POSITION_SCALE;
        renderer.prepared.camera.position.v[2] = -(int32_t)(10u + sample) * (int32_t)M2_POSITION_SCALE;
        renderer.prepared.camera.yaw = (int16_t)(sample % 360u);
        renderer.prepared.camera.pitch = (int16_t)((int16_t)(sample % 121u) - 60);
        renderer.prepared.camera.roll = (int16_t)-renderer.prepared.camera.pitch;
        for (uint8_t row = 0u; row < 8u; ++row)
        {
            switch (row)
            {
                case 0:
                    snprintf(expected, sizeof(expected), "NON-FLIGHT DIAGNOSTIC M2 UNBANKED");
                    break;
                case 1:
                    snprintf(expected, sizeof(expected), "TICK %08X CMD %08X",
                             renderer.snapshot.tick, renderer.snapshot.commands);
                    break;
                case 2:
                    snprintf(expected, sizeof(expected), "GEN %08X CAM %08X",
                             renderer.generation, renderer.prepared.camera.revision);
                    break;
                case 3:
                    snprintf(expected, sizeof(expected), "AGE AT TEXT %08X F %02X REJ %08X",
                             renderer.source_age_at_text, renderer.snapshot.fault, renderer.rejected);
                    break;
                case 4:
                    snprintf(expected, sizeof(expected), "CAM N%+06d E%+06d H%+05d FT",
                             renderer.prepared.camera.position.v[0] / (int32_t)M2_POSITION_SCALE,
                             renderer.prepared.camera.position.v[1] / (int32_t)M2_POSITION_SCALE,
                             -renderer.prepared.camera.position.v[2] / (int32_t)M2_POSITION_SCALE);
                    break;
                case 5:
                    snprintf(expected, sizeof(expected), "YAW%+04d PITCH%+03d ROLL%+03d",
                             renderer.prepared.camera.yaw, renderer.prepared.camera.pitch,
                             renderer.prepared.camera.roll);
                    break;
                case 6:
                    snprintf(expected, sizeof(expected), "ALTITUDE: NOT IMPLEMENTED");
                    break;
                default:
                    snprintf(expected, sizeof(expected), "               AIRSPEED: NOT IMPLEMENTED");
                    break;
            }
            size_t length = strlen(expected);
            assert(length <= 40u);
            m2rb_text_row(&renderer, row);
            assert(memcmp(renderer.text, expected, length) == 0);
            for (size_t column = length; column < 40u; ++column)
            {
                assert(renderer.text[column] == ' ');
            }
            ++comparisons;
        }
    }
    printf("TEXT PASS: %u independent exact rows; all counters, signs and validity placement\n", comparisons);
    return 0;
}
