/* Transient capture uses canonical low-memory hot-state RAM. Startup text
 * aliases it only BEFORE acquisition; final text lives in the HUD allocation. */
SECTIONS {
 .r0fc_capture 0x0300 (NOLOAD) : { KEEP(*(.r0fc_capture)) }
 .r0fc_hot 0x17A0 (NOLOAD) : { KEEP(*(.r0fc_hot)) }
}
INSERT AFTER .noinit;
ASSERT(SIZEOF(.r0fc_capture) == 5280, "CF001 capture length")
ASSERT(ADDR(.r0fc_capture) + SIZEOF(.r0fc_capture) <= 0x1900,
       "CF001 capture overlaps results")
ASSERT(ADDR(.r0fc_hot) + SIZEOF(.r0fc_hot) <= 0x1900, "CF001 hot state overlaps results")
