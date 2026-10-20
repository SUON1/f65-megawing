// Link-only reachability probe. Not an executable platform admission.
#include "m2_fixture.h"
#include "m2_geometry.h"

M2Camera m2_probe_camera = {{{-4500L * M2_POSITION_SCALE, 0,
                              -300L * M2_POSITION_SCALE}}, 0, -5, 0, 1u};
M2Registration m2_probe_record;
M2Point m2_probe_first;
M2Point m2_probe_last;
M2Line m2_probe_line;
M2Surface m2_probe_surface;
M2Pixel m2_probe_pixels[M2_RASTER_POINTS];
volatile uint8_t m2_probe_status;
volatile uint8_t m2_probe_index;
uint16_t m2_probe_count;

volatile uint32_t m2_probe_digest;

static void consume(const volatile void *data, uint16_t size)
{
    const volatile uint8_t *bytes = data;
    for (uint16_t i = 0u; i < size; ++i)
    {
        m2_probe_digest = (m2_probe_digest * 33u) ^ bytes[i];
    }
}

int main(void)
{
    m2_probe_status = m2_fixture_segment(1u, m2_probe_index,
                                         &m2_probe_first, &m2_probe_last);
    m2_probe_status = m2_surface_query(1u, &m2_probe_first, &m2_probe_surface);
    m2_probe_status = (uint8_t)m2_project_segment(&m2_probe_camera,
                       &m2_probe_first, &m2_probe_last, &m2_probe_line);
    m2_probe_status = m2_raster_line(&m2_probe_line, m2_probe_pixels,
                                     M2_RASTER_POINTS, &m2_probe_count);
    m2_probe_status = (uint8_t)m2_ground_sample(&m2_probe_camera, 0u, 0u);
    m2_probe_status = m2_registration(&m2_probe_camera, 1u, 600u, 0u,
                                      &m2_probe_record);
    m2_probe_status = m2_pair_eligible(&m2_probe_record, &m2_probe_record, 1u, 1u);
    consume(&m2_probe_camera, sizeof(m2_probe_camera));
    consume(&m2_probe_record, sizeof(m2_probe_record));
    consume(&m2_probe_first, sizeof(m2_probe_first));
    consume(&m2_probe_last, sizeof(m2_probe_last));
    consume(&m2_probe_line, sizeof(m2_probe_line));
    consume(&m2_probe_surface, sizeof(m2_probe_surface));
    consume(m2_probe_pixels, sizeof(m2_probe_pixels));
    consume(&m2_probe_count, sizeof(m2_probe_count));
    return 0;
}
