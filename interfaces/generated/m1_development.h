// Generated from interfaces/m1_development.json; do not edit.
#pragma once
#include <stdint.h>
// Source SHA-256: 942a639d5e5325f41618b458525b5fb79bb1c99ca3fafa960271e1ab7673214e
#define M1_TICK_HZ 100u
#define M1_STAGES 21u
#define M1_QUEUE_CAPACITY 8u
#define M1_SNAPSHOT_SLOTS 3u
#define M1_COLUMNS 80u
#define M1_ROWS 25u
#define M1_RENDER_ROWS_PER_SERVICE 1u
#define M1_DISPLAY_A 131072ul
#define M1_DISPLAY_B 196608ul
#define M1_COLOR 267911168ul
#define M1_ROM_BACKUP 134217728ul
#define M1_ROM_BACKUP_BYTES 131072ul
#define M1_RESIDENT_START 8193ul
#define M1_RESIDENT_END_EXCLUSIVE 32768ul
#define M1_SOFTWARE_STACK_START 49152ul
#define M1_SOFTWARE_STACK_END_EXCLUSIVE 53248ul
#define M1_RESERVE_START 360448ul
#define M1_RESERVE_END_EXCLUSIVE 393216ul
#define M1_HARDWARE_STACK_START 256ul
#define M1_HARDWARE_STACK_END_EXCLUSIVE 512ul
#define M1_BASE_PAGE_START 512ul
#define M1_BASE_PAGE_END_EXCLUSIVE 768ul
#define M1_PLATFORM_RESULT_START 6400ul
#define M1_PLATFORM_RESULT_END_EXCLUSIVE 8192ul
typedef struct
{
    uint32_t tick;
    uint8_t pressed;
    uint8_t released;
} M1Command;
typedef struct
{
    uint32_t tick;
    uint32_t commands;
    uint32_t checksum;
    uint8_t fault;
} M1Snapshot;
