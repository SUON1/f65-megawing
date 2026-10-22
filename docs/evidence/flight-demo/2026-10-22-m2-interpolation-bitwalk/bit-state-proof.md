# Interpolation bit/state equivalence

Let M = abs(delta), 0 <= M <= INT64_MAX, and let k = 0..63 count completed
steps. The working magnitude W_k = (M * 2^k) mod 2^64 has high bit equal to
(M >> (63-k)) & 1. W_0=M, and unsigned one-bit left shift establishes W_(k+1)
with defined modulo arithmetic. The 64th advance is valid; W_64=0 is unused.
Original signed delta is never shifted or changed, preserving sign restoration.

Let P_k be the prefix of the first k input bits. The original recurrence
maintains q_k=floor(P_k*n/d), r_k=(P_k*n) mod d. Equal selected bits and equal
initial zero state imply equal q/r at every step. Each update has temporary
remainder <= 3*d-2 < 2^48, and two subtraction tests restore r<d. With n<=d,
q_k<=P_k<=M<=INT64_MAX; final rounding cannot exceed M. The original ceil(d/2)
threshold is equivalent to the independent integer oracle's floor(d/2) bias.
Thus the unchanged rounding and signed narrowing remain exact and representable.

The invariant excludes INT64_MIN (the original signed negation precondition),
nonpositive denominators and ratios outside [0,1]. No public input domain is
expanded. Direct C checks compare both complete helper outputs with independent
integer expectations and assert the magnitude/bit invariant at all 64 positions
for every corpus case. No target instrumentation or ABI change is introduced.
