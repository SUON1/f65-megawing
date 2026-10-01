# Generated copy-limit source equivalence — 2026-09-29

After the capacity, overflow and short regression runs, the development C
probe replaced its local `255`-byte copy-buffer literal with generated
`R0FG1X_COPY_CHUNK_BYTES`. Fresh target builds for 327,680, 327,681 and
33,025 bytes produced PRGs **byte-identical** to the three already tested
programs. `equivalence.json` records exact lengths and SHA-256 values;
`prior-probe.c` and `current-probe.c` retain the source versions. Each new
`build.json` records its complete input hashes and passed target static
checks. No D81 or Xemu result was altered or repeated for this source-only
substitution.
