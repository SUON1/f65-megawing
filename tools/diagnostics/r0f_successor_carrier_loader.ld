MEMORY {
    ram (rw) : ORIGIN = 0x1000, LENGTH = 0x1000
}

SECTIONS {
    .text : { *(.text.r0fs_loader) } > ram
}

OUTPUT_FORMAT {
    SHORT(ORIGIN(ram))
    TRIM(ram)
}
