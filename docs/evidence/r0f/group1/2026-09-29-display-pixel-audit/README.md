# Group 1 saved-PNG display audit — 2026-09-29

This is a read-only diagnosis of the saved headless Xemu screenshots. The
earlier visual inspection appeared to omit different screen rows at different
capture times. The encoded PNGs do **not** show that variation. Do not use the
earlier observation as evidence of a target display defect.

The 90-second and 180-second digit-label runs have the same PRG SHA-256
(`b8ffb36ef0ad1b6dbfaa2e7e7e24a8e3656ae5fc90609ce472812c59dfb1c2d5`)
and byte-identical PNGs. The 90-second original-text run has the same PRG
SHA-256 (`e9649966665f5f398b4cfba192a9687522a367c3cd9c7c9fd8e7b1fd92781bc1`)
and byte-identical PNG as the frozen 180-second `irq-read-negative-07` run in
[`../2026-09-29-irq-display/`](../2026-09-29-irq-display/README.md). An
independent `ffmpeg` RGB decode found non-background glyph pixels in all six
text bands, at image rows 72–85, 104–117, 136–149, 168–181, 200–213 and
232–245 in each saved PNG. `pixel-audit.json` records exact hashes, counts and
the decoder version.

Each disposable run reached fault 107 at tick 3200 with a valid result CRC.
The returned D81 was independently checked for directory, chain, BAM and
content integrity; the actual `RSSTATE` matched the result-derived returning
SAVE. These remain direct-PRG development fault-injection runs, not a clean
Group 1 result, exact-carrier gate or physical display proof. No target source
change, SD write, physical run or tested-disk overwrite followed this audit.

The three run directories retain PRG, disposable D81, saved PNG and screen
text, result, memory dump, logs, injection and validation metadata, and
post-run extraction. `digits-90.py`, `digits-180.py` and `original-90.py`
retain the one-off run sources. `manifest.json` hashes all payloads in this
addendum as captured; the prior evidence freeze is unchanged.
