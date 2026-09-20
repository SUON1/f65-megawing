# Build Intent

Use this structure for substantive implementation, architecture-affecting work,
evidence-bearing work, or multi-file engineering work. A trivial typo or
mechanical maintenance task does not need a separate Build Intent file when the
approved task is already explicit.

A Build Intent may live in `WORK_IN_PROGRESS.md`, a task prompt, or a dedicated
task record when needed. This template provides consistency; it does not require
creating a permanent file for every task.

## Objective

What outcome is required?

## Why now

Why is this work being performed at this point in the project?

## Governing authority

Relevant approved specification, interface, decision, evidence, or
project-truth source.

## Scope

What this task may change.

## Non-scope

What this task must not change.

## Owner / subsystem

Primary code, data, or document owner affected.

## Contract and hardware impact

Identify as applicable:

- public/generated interface;
- memory ownership;
- register/clobber behavior;
- MAP/base-page;
- DMA;
- timing/deadline;
- IRQ/NMI; and
- persistent/serialized state.

Use `None` or `Not applicable` explicitly when appropriate.

## Validation

Required evidence tier and checks. Possible tiers include:

- documentation/static;
- host;
- target compile/link;
- Xemu;
- physical MEGA65; and
- human acceptance.

Do not imply one tier substitutes for another.

## Human decisions

Decisions that remain founder-owned. Use `None` when no decision is required.

## Completion condition

What must be true for this task to be ready for founder review.
