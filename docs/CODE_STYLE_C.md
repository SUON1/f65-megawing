# F-65 C Coding and Readability Standard

## Purpose and scope

F-65 C code must be easy for a technically capable human to read and understand later. Prefer clear, conventional C over clever C. Readability is part of correctness because target behavior, ownership, memory use, and hardware effects must remain reviewable.

> F-65's formatting and general readability conventions are influenced by the [CS50 C Style Guide](https://cs50.readthedocs.io/style/c/). F-65-specific embedded, deterministic-runtime, MEGA65 hardware, generated-interface, ABI, and measured-performance requirements remain controlling where they differ.

CS50 is a style influence, not a project authority. F-65 does not depend on CS50 tooling.

This guide applies to:

- new production code;
- new proof code;
- code that is materially modified; and
- deliberate readability or refactoring tasks.

Existing R0 proof/evidence-bearing code is not required to be reformatted or refactored solely to comply with this guide. Do not create a repository-wide style migration or disturb proven low-level code merely to make it prettier.

Architecture, generated interfaces, memory ledgers, public contracts, and measured hardware behavior remain authoritative over this style guide.

## Readability, ownership, and functions

- Use descriptive names that communicate purpose, units, ownership, and state.
- Keep functions small enough to have one primary responsibility.
- Prefer explicit control flow and predictable state changes.
- Keep pointer and buffer use bounded. Validate ranges and lengths before access.
- Handle failure explicitly where failure is possible; do not silently continue with invalid state.
- Prefer direct code to unnecessary abstraction.

For a major C source file, a technically capable reader should normally be able to determine quickly:

> What does this file own?

Related persistent state should have an identifiable owner. Global state must be deliberate, narrowly scoped, and have clear ownership.

For an important function, a reader should normally be able to determine:

> What does this function do, and what state does it change?

Avoid functions that silently perform multiple unrelated subsystem responsibilities. Important side effects should be apparent from naming, structure, documentation, or the governing interface contract.

## Naming, types, constants, and state

- Use `lower_snake_case` for normal private functions and variables.
- Use `UPPER_SNAKE_CASE` for macros and named constants.
- Keep governing generated and public names exactly as defined by the applicable interface or generated contract.
- Avoid cryptic abbreviations unless they are established project, aviation, hardware, MEGA65, or mathematical terminology.
- Use `uint8_t`, `uint16_t`, `uint32_t`, and signed counterparts where representation matters.
- Use wider intermediates before narrowing when overflow is possible, then apply the contract-defined range rule.
- Do not rely on implementation-defined structure packing, enum width, bit-field layout, or pointer size for ABI-visible, serialized, checksum, replay, or hardware-facing data.
- Prefer generated constants and layouts to handwritten duplicates.
- Give units in names or comments when values could otherwise be ambiguous.
- Keep mutable globals private to their owning file unless a documented interface requires exposure.
- Initialize state explicitly and avoid reusing one variable for unrelated meanings.

Examples:

```c
uint16_t current_track_count;
bool aircraft_ready;

void update_flight_controls(void);

#define MAX_AIRCRAFT 16
#define VIC_IV_BORDER_REGISTER 0xD020
```

Gameplay tuning values, thresholds, timing values, limits, and other important configuration parameters should be centralized where practical rather than scattered through unrelated implementation logic. This includes movement or control rates, AI thresholds, timing intervals, capacity limits, warning thresholds, tuning coefficients, presentation timing, and resource limits. Do not move existing R0 constants solely for style.

## Hardware-facing code

Use descriptive named constants for MEGA65 registers, addresses, masks, commands, and hardware values. A raw value is acceptable only when its meaning is immediate and local; otherwise name it.

```c
#define VIC_IV_BORDER_REGISTER 0xD020
#define SPRITE_ENABLE_MASK     0x01
```

Where a function interacts with MEGA65 hardware, comments or nearby contract documentation must identify relevant non-obvious effects, as applicable:

- registers used and preserved or clobbered registers;
- CPU-visible and physical memory ranges;
- MAP and base-page state;
- DMA submission, blocking, ownership, and completion behavior;
- IRQ behavior and NMI assumptions;
- hardware ownership and exclusion requirements; and
- restoration obligations before return.

Trivial wrappers do not need large documentation blocks. Document the effects that a reviewer cannot safely infer from ordinary C.

Ordinary C pointers must not be used as substitutes for project-defined physical or far-memory representations. Generated contracts and platform wrappers remain the source of truth for public layout and hardware access.

## Functions and control flow

- Prefer early validation or a clear cleanup path over deeply nested logic.
- Keep conditionals readable; introduce a well-named intermediate value when an expression hides intent.
- Avoid hidden fallthrough, surprising mutation in expressions, and dependence on unspecified evaluation order.
- Keep cleanup and restoration obligations visible on every exit path.
- Do not combine unrelated work only to reduce function count.

Discourage important state changes inside complex expressions. Prefer explicit statements when they make ordering or state mutation clearer.

```c
state++;
table_index = state & TABLE_INDEX_MASK;

buffer[index] = table[table_index];
index++;
```

Use judgment; do not mechanically expand simple expressions that are already obvious.

## Comments and documentation

Comments should explain why code exists, hardware requirements, unusual ordering, ownership, side effects, constraints, evidence-backed exceptions, or non-obvious failure behavior. Do not narrate obvious syntax or preserve stale implementation descriptions.

- Put normal implementation comments above the code they describe rather than at the end of a line.
- Use `// `, with one space after the slashes, for ordinary short comments.
- Give important source and header files a concise responsibility comment when the filename alone is insufficient.
- Give important non-trivial functions concise documentation when their contract or side effects are not obvious.
- Do not establish a fixed comment frequency or require comments every few lines.

```c
// Preserve the last valid radar track until the coast timer expires.
// This avoids dropping a contact on a single missed scan.
if (track->coast_ticks < TRACK_COAST_LIMIT)
{
    track->coast_ticks++;
}
```

Avoid comments that merely translate obvious syntax into English.

Do not retain large blocks of commented-out obsolete implementation as version control. Git history preserves prior implementations. Short temporary comments during active work are acceptable, but completed work should not accumulate disabled legacy code.

## Macros and abstraction

Keep macros straightforward and unsurprising. Prefer typed functions, enums, and constants when they express the same intent without target-cost or compatibility harm. Parenthesize macro parameters and results where evaluation requires it, and never hide control flow or repeated side effects in a macro.

Avoid:

- framework-building without a demonstrated need;
- generic callback systems merely for style;
- object-like abstraction layers around simple state;
- macro metaprogramming; and
- premature generalization.

Direct, readable C is preferred. Extract an abstraction when it clarifies real repeated behavior or enforces an existing contract.

## Performance and hardware exceptions

Readable C is the default. If a measured timing, memory, DMA, compiler, or hardware constraint requires less-readable code:

- keep the required optimization;
- document why the complexity exists;
- identify the governing constraint or measurement when practical;
- preserve the same public contract; and
- run the required validation.

Do not make code obscure merely because it might someday be performance-sensitive. Measure first unless the platform contract itself requires low-level handling. Do not simplify proven low-level code merely to make it prettier.

## Formatting baseline

Use these formatting conventions for new or materially modified C, except where generated or public declarations retain their governing form.

### Braces and indentation

- Put opening and closing braces on their own lines for functions, `if` / `else`, `switch`, `for`, `while`, `do` / `while`, and structures.
- Use braces even for normal single-statement control blocks unless a narrowly justified exception is clearer.
- Indent with 4 spaces per level. Do not use literal tab characters for C indentation.

```c
if (system_ready)
{
    enable_system();
}
else
{
    report_system_fault();
}
```

### Spacing and line length

- Use spaces around normal binary operators and one space after commas.
- Do not put spaces immediately inside parentheses.
- Use one normal statement per line.
- Treat approximately 80 characters as a preferred soft target and 100 characters as the normal upper bound.
- Do not break lines mechanically when doing so makes hardware-oriented, generated, mathematical, tabular, or contract-related code harder to understand. Readability controls.

### Declarations, headers, and loops

- Prefer `uint8_t *buffer;` rather than `uint8_t* buffer;`.
- Order includes as standard or system headers, a blank line, then project or generated headers. Alphabetize within each group where practical.
- Do not reorder generated files merely for style.
- Declare variables close to where they are first needed and keep their scope as narrow as practical. Do not collect all locals at function start merely from old C convention unless the compiler or toolchain requires it.
- `i`, `j`, and `k` are acceptable for small obvious local loops. Use descriptive iteration names when the identity being iterated matters.
- Functions with no arguments should use `function_name(void)`, unless the actual target or runtime entry contract requires another signature.

```c
int main(void)
{
    return 0;
}
```

```c
#include <stdint.h>
#include <string.h>

#include "f65_entity.h"
#include "f65_platform.h"
#include "f65_world.h"
```

### Switch statements

Use visibly indented cases and explicit `break` statements where appropriate. Intentional fallthrough should be rare and explicitly commented.

```c
switch (flight_mode)
{
    case FLIGHT_MODE_CRUISE:
        update_cruise_mode();
        break;

    case FLIGHT_MODE_COMBAT:
        update_combat_mode();
        break;

    default:
        report_invalid_flight_mode();
        break;
}
```

No formatter or linter is mandated. Do not add `style50`, `clang-format`, another formatter, or another linter without a separate compatibility decision.

## Review expectations

New or materially modified C should be reviewed for ownership, function purpose, state changes, bounds, failure behavior, generated-contract use, and hardware restoration obligations as applicable. Validation must remain proportional to the affected contract and evidence tier; formatting alone never substitutes for compilation, host checks, Xemu, or physical evidence when those are required.
