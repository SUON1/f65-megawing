#include "m1_input.h"

uint8_t m1_input_sample(M1Input *input, M1Core *core, uint8_t down)
{
    down &= 1u;
    uint8_t change = (uint8_t)(down ^ input->previous);
    if (change == 0u)
    {
        return 1u;
    }
    M1Command command = {core->tick + 1u, (uint8_t)(change & down),
                         (uint8_t)(change & input->previous)};
    if (!m1_command(core, command))
    {
        return 0u;
    }
    input->previous = down;
    return 1u;
}
