SECTIONS {
    /* Every code byte and data/constant byte required while a temporary
     * 0x8000-0xbfff MAP window is active belongs in this accessible output
     * section. T02 has no separate protected data/constant input today. */
    .r0fs_protected : {
        KEEP(*(.text.r0fs_protected))
        KEEP(*(.rodata.r0fs_protected))
        KEEP(*(.data.r0fs_protected))
    }
}
INSERT BEFORE .text;

ASSERT(ADDR(.r0fs_protected) >= 0x2001,
       "successor protected code below resident start")
ASSERT(ADDR(.r0fs_protected) + SIZEOF(.r0fs_protected) <= 0x8000,
       "successor protected code covered by MAP window")
