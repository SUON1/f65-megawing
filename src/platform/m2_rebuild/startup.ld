/* Reset-only private baseline: early normalization replaces stock port writes
 * and excludes CHROUT/final ROM restoration. SDK stack/BSS initializers remain.
 */
SECTIONS {
    /DISCARD/ : { *(.init.010) *(.init.250) *(.fini.990) }
}
INSERT BEFORE .text;
