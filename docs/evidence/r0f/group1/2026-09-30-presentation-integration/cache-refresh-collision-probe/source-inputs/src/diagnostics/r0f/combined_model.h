#ifndef R0F_COMBINED_MODEL_H
#define R0F_COMBINED_MODEL_H
#include <stdint.h>
#include "r0f_combined.h"
typedef struct {
  uint16_t x[R0FC_ENTITIES], y[R0FC_ENTITIES], z[R0FC_ENTITIES];
  uint16_t command[9], next[9], effects[R0FC_EFFECTS];
  uint16_t tick, environment;
  uint32_t checksum;
  uint8_t events[R0FC_QUEUE_CAPACITY], event_count, queue_high, rejected;
} r0fc_model;
typedef struct {
  uint8_t state[R0FC_SNAPSHOT_COUNT], data[R0FC_SNAPSHOT_COUNT][R0FC_SNAPSHOT_BYTES];
  uint16_t skipped, published, acquired;
  uint8_t high, reading;
} r0fc_snapshots;
typedef struct { uint8_t state, pressed, released; } r0fc_edges;
uint8_t r0fc_edge_sample(r0fc_edges *e,uint8_t state);
uint8_t r0fc_edge_consume(r0fc_edges *e);
void r0fc_reset(r0fc_model *m);
void r0fc_tick(r0fc_model *m);
uint8_t r0fc_event(r0fc_model *m, uint8_t entity);
void r0fc_snap_reset(r0fc_snapshots *s);
uint8_t r0fc_publish(r0fc_snapshots *s, const r0fc_model *m);
uint8_t r0fc_acquire(r0fc_snapshots *s);
void r0fc_release(r0fc_snapshots *s);
uint8_t r0fc_range(uint32_t p, uint16_t n, uint8_t write, uint8_t reclaimed);
uint8_t r0fc_dma_encode(uint8_t *out, uint32_t src, uint32_t dst, uint16_t n, uint8_t reclaimed);
uint32_t r0fc_hash(uint32_t h, uint16_t value);
uint32_t cfratio(uint32_t a,uint32_t b,uint32_t denominator,uint8_t shift);
#endif
