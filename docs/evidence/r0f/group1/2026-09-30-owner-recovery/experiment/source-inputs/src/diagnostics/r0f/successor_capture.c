#include "combined_platform.h"
#include "r0f_successor_integration.h"
#include "successor_capture.h"

// Two 256-byte pages expose the existing 512-byte record after cleanup.
// Writes only through the inherited final-screen helpers; no DMA or storage.
void r0fsi_capture_page(uint8_t page)
{
    if (page >= 2u)
    {
        return;
    }
    cfscreen();
    cfline(1u, "R0FCAP13 RESULT CAPTURE - NOT R0-F ACCEPTANCE");
    // Clear the inherited development banner before the shorter heading.
    cfline(3u, "                                                                                ");
    cfline(3u, "PAGE    OF 02   CRC32:");
    cfhex(3u, 5u, (uint8_t)(page + 1u), 2u);
    cfhex(3u, 22u, cfget32(R0FSI_O_CRC32), 8u);
    for (uint16_t row = 0u; row < 16u; row++)
    {
        uint16_t offset = (uint16_t)((uint16_t)page * 256u + row * 16u);
        cfhex((uint8_t)(5u + row), 0u, offset, 4u);
        for (uint8_t column = 0u; column < 16u; column++)
        {
            cfhex((uint8_t)(5u + row), (uint8_t)(6u + column * 3u),
                  cfresult[offset + column], 2u);
        }
    }
    cfline(23u, "N: NEXT PAGE   S: SUMMARY   PHOTOGRAPH BOTH PAGES");
    cfline(24u, "CAPTURE ONLY. NO NEW DISK WRITE. RESET TO EXIT.");
}
