#include "m2_rebuild_input.h"

uint16_t m2rb_input_edges(M2RebuildInput *input, uint16_t down)
{
    uint16_t edges = (uint16_t)(down & (uint16_t)~input->previous);
    input->previous = down;
    return edges;
}
