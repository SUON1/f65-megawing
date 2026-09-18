extern void r0f_run(void);
#ifdef R0F_CIA_TIMING
extern void r0f_timing_run(void);
#ifdef R0F_RAW_CAPTURE
extern void r0f_capture_run(void);
int main(void) { r0f_run(); r0f_timing_run(); r0f_capture_run(); }
#else
int main(void) { r0f_run(); r0f_timing_run(); for (;;) {} }
#endif
#else
int main(void) { r0f_run(); for (;;) {} }
#endif
