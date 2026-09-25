# Physical chooser incident — 2026-09-21

Status: **R0FSUCC10.D81 physical copy INVALID — DO NOT USE.**

Owner supplied these three unmodified photographs in the task. They show:

1. `chooser-ff.jpg`: selected `R0FSUCC10.D81` and `ERROR CODE FF` in the
   physical disk chooser. This is an attach-stage failure; target execution
   and physical R0-F success are not established.
2. `eight-character-limit.jpg`: native image creation dialog showing
   `R0FSUCC1`. Owner reports that a ninth character could not be entered.
3. `native-slot-name.jpg`: creation dialog containing `R0FSUC10`. Owner reports
   a freshly formatted blank slot. The photograph itself shows name entry,
   not formatting completion. The mounted card currently has no such root
   entry; clarification is pending. Never overwrite another similarly named
   file or infer that an unrelated blank belongs to this task.

SHA-256 identities of raw owner evidence:

| File | SHA-256 |
|---|---|
| chooser-ff.jpg | `d5212126f3d83d3078c578f64f05dcef75b8499716bc59cf740cd99b5ad80f00` |
| eight-character-limit.jpg | `395e5950d0a937eb1e6be9594fc88c4ab25c023f6fdef9c9d624a38d5b0954bd` |
| native-slot-name.jpg | `88b0f427c4ecdf4d7a941abbaa070df84a4ef929eaa1aec3e075e684c6753398` |

Read-only host observation: `/Volumes/MEGA65FDISK/R0FSUCC10.D81` is 819,200
bytes and hashes to
`3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`, matching
the canonical exactly. Internal D81 structure passes the existing foundation
comparison against retained physical control `F65BLK02.D81`, SHA-256
`b13853a7ddaf3bf26dfcaceb7e4466ab2d58702b96bfcbe9ae62c7db56ed3d82`.
The control has a different workload; byte differences do not diagnose a
construction defect. Its current SD copy is not assumed to equal the retained
pre-run control image.

Confirmed workflow defect: the T04 builder admitted a nine-character basename
that the existing SD transfer helper rejects. Earlier assistant speculation
about pasted whitespace causing that rejection was incorrect. The filename
defect does not by itself prove the exact physical FF cause; long-name alias,
FAT extent and installed platform evidence remain necessary.

The failed copy remains untouched for inspection. Neither new candidate is
a renamed or patched failed image; both are fresh single-session constructions
from the hash-verified retained T04 payloads, using compliant host names.
