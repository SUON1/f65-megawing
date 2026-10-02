#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "r0f_combined.h"
#include "group1_pool_owners.h"

// The included functions are extracted verbatim from the candidate platform
// source by the host controller. Only register, clock/copy and metric edges
// are mocked; this is not physical PCM or DMA evidence.
static uint8_t registers[65536], block[255];
static uint8_t pcm_on, pcm_last, audio_frame, audio_cache_valid, copy_ok = 1u;
static uint32_t service_last;
uint8_t cffault;
#define CFREG(address) registers[address]

static uint32_t cfnow(void) { return 100u; }
static void cfadd(uint16_t offset, uint32_t value) { (void)offset; (void)value; }
static uint32_t cfget32(uint16_t offset) { (void)offset; return 0u; }
static void cfput32(uint16_t offset, uint32_t value) { (void)offset; (void)value; }
static uint8_t cfcopy(uint32_t physical, uint8_t *bytes, uint8_t length, uint8_t to_chip)
{
    assert(physical == R0FC_AUDIO && length == 255u && to_chip == 1u);
    for (unsigned index = 0u; index < length; index++)
    {
        assert(bytes[index] == 112u + (index & 31u));
    }
    return copy_ok;
}

#include "audio_owner_under_test.inc"

static unsigned field(uint8_t owner, uint8_t offset)
{
    uint8_t bytes[R0FG1_POOL_EPOCH_BYTES];
    r0fg1_owners_encode(bytes);
    unsigned at = owner * R0FG1_POOL_RECORD_BYTES + offset;
    return (unsigned)bytes[at] | (unsigned)bytes[at + 1u] << 8u;
}

int main(void)
{
    assert(r0fg1_owners_begin());
    cfaudio_begin();
    assert(pcm_on == 1u && CFREG(0xd720u) == 0xe2u && !cffault);
    assert(field(R0FG1_POOL_AUDIO_CACHE, R0FG1_POOL_W_SAMPLES) == 3u);
    assert(field(R0FG1_POOL_AUDIO_CACHE, R0FG1_POOL_W_FULL_SAMPLES) == 1u);
    cfaudio_service(1u);
    assert(!pcm_on && !CFREG(0xd720u));
    cfaudio_service(0u);
    assert(pcm_on && CFREG(0xd720u) == 0xe2u);
    cfaudio_stop();
    cfaudio_begin();
    assert(field(R0FG1_POOL_AUDIO_CACHE, R0FG1_POOL_W_SAMPLES) == 5u);
    assert(field(R0FG1_POOL_AUDIO_CACHE, R0FG1_POOL_W_FULL_SAMPLES) == 2u);
    copy_ok = 0u;
    cfaudio_begin();
    assert(!pcm_on && !audio_cache_valid);
    assert(field(R0FG1_POOL_AUDIO_CACHE, R0FG1_POOL_W_SAMPLES) == 6u);
    assert(field(R0FG1_POOL_AUDIO_CACHE, R0FG1_POOL_W_FULL_SAMPLES) == 2u);
    assert(field(R0FG1_POOL_PCM_CHANNELS, R0FG1_POOL_W_PEAK) == 1u);
    assert(field(R0FG1_POOL_PCM_CHANNELS, R0FG1_POOL_W_FULL_SAMPLES) == 0u);
    assert(!cffault);
    puts("actual audio functions: start, stop, warning, refill and failed-copy observations PASS");
    return 0;
}
