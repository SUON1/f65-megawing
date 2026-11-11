// Shared byte descriptors retain independent expected/candidate field values.
#include <stddef.h>
#include <string.h>

#include "m2_rebuild.h"
#include "m2_record_private.h"

_Static_assert(offsetof(M2Camera, yaw) == 12 && offsetof(M2Camera, pitch) == 14
    && offsetof(M2Camera, roll) == 16, "camera field run changed");
_Static_assert(sizeof(M2RebuildRenderer) < 32768, "descriptor offset flag overlap");

uint8_t m2_camera_same(const M2Camera *first, const M2Camera *last)
{
    // The first18 bytes are exactly position/yaw/pitch/roll; padding before
    // revision is intentionally excluded on host ABIs with four-byte alignment.
    return (uint8_t)(first != 0 && last != 0 && memcmp(first, last, 18u) == 0
        && memcmp(&first->revision, &last->revision, sizeof(first->revision)) == 0);
}

typedef struct
{
    uint16_t source;
    uint8_t destination;
    uint8_t count;
} Field;

typedef struct
{
    uint32_t fixture;
    uint32_t projection;
    uint32_t composition;
    uint32_t outer;
    uint16_t zero;
} FixedFields;

#define RECORD_OFFSET(member) offsetof(M2RebuildBundle, registration.member)
#define CONSTANT_OFFSET(member) (32768u | offsetof(FixedFields, member))

uint8_t m2_bundle_fields(M2RebuildRenderer *renderer, uint8_t compare)
{
    static const FixedFields fixed = {
        M2_FIXTURE_REVISION, M2_PROJECTION_REVISION, M2_COMPOSITION_REVISION,
        M2RB_COMPOSITION_REVISION, 0u
    };
    static const Field fields[] = {
        {offsetof(M2RebuildRenderer, prepared.camera), RECORD_OFFSET(camera), 18},
        {offsetof(M2RebuildRenderer, prepared.camera.revision), RECORD_OFFSET(camera.revision), 4},
        {offsetof(M2RebuildRenderer, prepared.rotation), RECORD_OFFSET(transform), sizeof(M2Transform)},
        {offsetof(M2RebuildRenderer, generation), RECORD_OFFSET(generation), 4},
        {offsetof(M2RebuildRenderer, snapshot.tick), RECORD_OFFSET(source_tick), 4},
        {CONSTANT_OFFSET(fixture), RECORD_OFFSET(fixture_revision), 4},
        {CONSTANT_OFFSET(projection), RECORD_OFFSET(projection_revision), 4},
        {CONSTANT_OFFSET(composition), RECORD_OFFSET(composition_revision), 4},
        {CONSTANT_OFFSET(zero), RECORD_OFFSET(view_id), 2},
        {CONSTANT_OFFSET(zero), RECORD_OFFSET(tier_id), 2},
        {offsetof(M2RebuildRenderer, destination), RECORD_OFFSET(store), 1},
        {CONSTANT_OFFSET(outer), offsetof(M2RebuildBundle, composition_revision), 4},
        {offsetof(M2RebuildRenderer, snapshot.checksum), offsetof(M2RebuildBundle, checksum), 4}
    };
    if (compare > 1u || renderer->prepared.ready != 1u || renderer->generation == 0u
        || renderer->destination > 1u || (compare && renderer->tile_index != 960u))
    {
        return 0u;
    }
    uint8_t *destination = (uint8_t *)&renderer->bundles[renderer->destination];
    for (uint8_t field = 0u; field < sizeof(fields) / sizeof(fields[0]); ++field)
    {
        uint16_t offset = fields[field].source;
        const uint8_t *source = offset & 32768u
            ? (const uint8_t *)&fixed + (offset & 32767u)
            : (const uint8_t *)renderer + offset;
        uint8_t *target = destination + fields[field].destination;
        for (uint8_t byte = 0u; byte < fields[field].count; ++byte)
        {
            if (compare)
            {
                if (target[byte] != source[byte])
                {
                    return 0u;
                }
            }
            else
            {
                target[byte] = source[byte];
            }
        }
    }
    return 1u;
}
