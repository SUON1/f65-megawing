/* R0-F writes screen codes directly and uses no SDK character I/O.
 * Pinned SDK commodore/char-conv.c adds a .init.250 CHROUT call with
 * B already relocated. Exclude that initializer; do not admit ROM calls.
 * The R0-F static gate checks the final executable for ROM calls.
 */
SECTIONS { /DISCARD/ : { *(.init.250) } }
INSERT BEFORE .text;
