# Group 1 IRQ/space local checkpoint — presentation open

The root source/binary freeze is the current 36,473-byte program:
`ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30`.
Rebuilding after removal of the attribute experiment reproduces it exactly.

- `irq-ntsc-07/`, `irq-pal-06/`: 3200 ticks, actual returning SAVE and trace,
  zero nominal misses and no cohort below 20 Hz; 18 corruption cases each.
- `capsule-negative-06/`, `nmi-negative-06/`, `irq-read-negative-07/`:
  integrated fault lockout and zero export. Screenshots have the open
  presentation limitation described in the report; state validation is separate.
- `source-inputs/`, root build/map/symbol/disassembly files: current source freeze.
- `development/`: earlier and diagnostic revisions. Each retains its own
  injection/build identity; they are not all products of the root source.
  Register diagnostics 02 stopped in the live reader and are not terminal data.
  Diagnostics 03 use an isolated terminal stub. The visible-window attempt
  timed out without inspectable output; it is not visual evidence.
- `final/`: **superseded** attribute experiment, despite its historical name;
  see its README. The root build is current.
- `pinned-xemu/`: exact-source excerpts; the header was added for attribute
  inspection. The manifest hashes it along with the other evidence.
- `preservation.json`: rechecked earlier freezes and prebuild dirty evidence.

The failure screen intermittently lacks labels in saved screenshots despite
correct text/font/color RAM and matching VIC registers. Do not promote a
single complete screenshot to operator-presentation acceptance. IRQ body-read
resolution also remains unresolved in this pinned Xemu build.

Disposable multi-gigabyte SD clones remain under the original build run paths;
small PRGs, D81s, actual files, memory, screenshots and logs are retained here.
No host D81 here is a delivery candidate. No SD write or physical run occurred.
Full Group 1 and R0-F acceptance remain open. See the frozen checkpoint report
and `docs/reports/R0-F_GROUP1_IRQ_SPACE.md` for scope and exact commands.
