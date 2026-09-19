#ifndef R0F_RESUME_MODEL_H
#define R0F_RESUME_MODEL_H
#include <stdint.h>
#include "r0f_resume.h"
uint8_t r0fr_transition(uint8_t state, uint8_t event);
uint8_t r0fr_storage_allowed(uint8_t state, uint8_t restored, uint8_t fault);
#endif
