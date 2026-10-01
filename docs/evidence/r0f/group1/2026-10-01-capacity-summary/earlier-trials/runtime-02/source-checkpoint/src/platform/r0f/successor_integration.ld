SECTIONS {
    .r0fs_protected : {
        KEEP(*(.text.r0fs_protected))
        KEEP(*(.text.r0f_pf))
        KEEP(*(.rodata.r0fs_protected))
        KEEP(*(.data.r0fs_protected))
        KEEP(*(.r0fs_protected_data))
    }
}
INSERT BEFORE .text;

ASSERT(ADDR(.r0fs_protected) >= 0x2001,
       "successor protected content below resident start")
ASSERT(ADDR(.r0fs_protected) + SIZEOF(.r0fs_protected) <= 0x8000,
       "successor protected code/data covered by MAP window")
