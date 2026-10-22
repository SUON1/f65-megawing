// Graphics-owned immutable context between successful prepare and cancellation.
// Private workspace, never accepted from a public record or serialized input.
#pragma once
#include "m2_geometry.h"
struct M2Prepared
{
    M2Camera camera;
    M2Transform rotation;
    uint8_t ready;
};
uint8_t m2_prepare(struct M2Prepared *prepared, const M2Camera *camera);
int8_t m2_project_prepared(const struct M2Prepared *prepared,
                          const M2Point *first, const M2Point *last, M2Line *line);
int8_t m2_ground_prepared(const struct M2Prepared *prepared, uint16_t x, uint16_t y);
uint8_t m2_registration_prepared(const struct M2Prepared *prepared,
                                 uint32_t generation, uint32_t tick, uint8_t store,
                                 M2Registration *record);

// Private captured-owner comparison; does not reconstruct a caller's matrix.
uint8_t m2_registration_matches_prepared(const struct M2Prepared *prepared,
    const M2Registration *record, uint32_t generation, uint32_t tick, uint8_t store);
