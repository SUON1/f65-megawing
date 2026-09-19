package f65.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.HexFormat;

/** Host-only source-model cross-check. NEVER grants calibrated-time validity. */
public final class R0FClockPreflight {
    private static final String CORE = "b5c770c6bab8a886e07b5c0d3df4f19d1aa0632f";
    private static final String PROFILE = "b5c770c6-ntsc-526-no-debug";

    /* frame_generator.vhdl defaults; pixel_driver.vhdl frame60 does not
       override cycles_per_raster_1mhz. Do not substitute the comment's 65. */
    private static final int WIDTH = 858, HEIGHT = 526, X_ZERO = 858 - 46;
    private static final int CYCLES_PER_PIXEL = 3, PHI_PER_PAIR = 63;

    /* Only the PHI-toggle producer, not a model of CPU/CIA/bus latency or CDC.
       Reads of old state and last-assignment precedence follow the VHDL.
       No oscillator frequency is assumed or inferred from a signal name. */
    static final class FrameModel {
        int x, y = HEIGHT - 3, pixelCounter, accumulator, remaining;
        long pulses;
        boolean step() {
            int nextAccumulator = (accumulator & 65535)
                    + 1 + 65536 * PHI_PER_PAIR / (WIDTH * 2 * CYCLES_PER_PIXEL);
            int nextRemaining = remaining;
            if ((accumulator & 65536) != 0 && remaining != 0) {
                pulses++;
                nextRemaining--;
            }
            boolean frame = false;
            if (pixelCounter != CYCLES_PER_PIXEL - 1) {
                pixelCounter++;
            } else {
                pixelCounter = 0;
                if (x == X_ZERO && remaining == 0) nextRemaining = PHI_PER_PAIR;
                if (x < WIDTH - 1) {
                    x++;
                } else {
                    x = 0;
                    if (y < HEIGHT - 1) {
                        y++;
                    } else {
                        y = 0;
                        nextAccumulator = 0;
                        frame = true;
                    }
                }
            }
            accumulator = nextAccumulator;
            remaining = nextRemaining;
            return frame;
        }
        long nextFrame() {
            long start = pulses;
            int limit = WIDTH * HEIGHT * CYCLES_PER_PIXEL;
            for (int i = 0; i < limit; i++) if (step()) return pulses - start;
            throw new IllegalStateException("source-model frame bound");
        }
    }

    static long[] sourceFrames() {
        FrameModel model = new FrameModel();
        // Discard initial partial frame and settling frames. Retain every count.
        for (int i = 0; i < 4; i++) model.nextFrame();
        long[] frames = new long[32];
        for (int i = 0; i < frames.length; i++) frames[i] = model.nextFrame();
        return frames;
    }

    static String digest(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    static String inspect(byte[] capture, String expectedSha256, String profile) throws Exception {
        R0FTimingOracle.require(PROFILE.equals(profile), "unsupported source profile; no mode auto-detection");
        R0FTimingOracle.require(expectedSha256.matches("[0-9a-f]{64}"), "expected SHA-256 syntax");
        R0FTimingOracle.require(digest(capture).equals(expectedSha256), "capture SHA-256 mismatch");
        R0FTimingOracle.validate(capture);
        long[] frames = sourceFrames();
        long modelBefore = 0, modelAfter = 0;
        for (int i = 0; i < 16; i++) {
            modelBefore += frames[i];
            modelAfter += frames[i + 16];
        }
        long before = R0FTimingOracle.u32(capture, 152);
        long after = R0FTimingOracle.u32(capture, 240);
        // Residuals are observations, NOT a made-up calibration tolerance.
        return """
                {
                  "schema": "r0f-clock-source-preflight-v1",
                  "captureSha256": "%s",
                  "captureValidation": "PASS_RAW_COUNTS_ONLY",
                  "sourceCommit": "%s",
                  "declaredProfile": "%s",
                  "sourceAttribution": "CANDIDATE_NOT_INSTALLED_BITSTREAM_VERIFICATION",
                  "frameModelScope": "PHI_TOGGLE_PRODUCER_ONLY_NO_CPU_CIA_CDC_OR_POLLING_MODEL",
                  "sourceModel16FramesBefore": %d,
                  "sourceModel16FramesAfter": %d,
                  "observed16FramesBefore": %d,
                  "observed16FramesAfter": %d,
                  "observedMinusModelBefore": %d,
                  "observedMinusModelAfter": %d,
                  "calibrationValid": false,
                  "calibrationBlocker": "NO_VERIFIED_FREQUENCY_REFERENCE_UNCERTAINTY_OR_END_TO_END_CLOCK_MODEL",
                  "microsecondsPerCount": null,
                  "cpuCyclesPerCount": null,
                  "real100HzVerified": false,
                  "combinedHardwareReady": false
                }
                """.formatted(expectedSha256, CORE, profile, modelBefore, modelAfter,
                        before, after, before - modelBefore, after - modelAfter);
    }

    static void selfTest(byte[] capture, String expectedSha256) throws Exception {
        long[] frames = sourceFrames();
        for (long count : frames) {
            // Independent steady-state quota expectation; not capture-derived.
            R0FTimingOracle.require(count == (long) HEIGHT / 2 * PHI_PER_PAIR, "source-model quota");
        }
        String report = inspect(capture, expectedSha256, PROFILE);
        R0FTimingOracle.require(report.contains("\"calibrationValid\": false")
                && report.contains("\"microsecondsPerCount\": null")
                && report.contains("\"cpuCyclesPerCount\": null")
                && report.contains("\"combinedHardwareReady\": false"), "false qualification");
        int rejected = 0;
        for (int offset : new int[]{0, 4, 151, 152, 240, 255, 256, 11135}) {
            byte[] bad = capture.clone();
            bad[offset] ^= 1;
            try { inspect(bad, expectedSha256, PROFILE); }
            catch (IllegalArgumentException expected) { rejected++; continue; }
            throw new IllegalStateException("accepted altered capture");
        }
        for (String badProfile : new String[]{"PAL", "NTSC", "", CORE}) {
            try { inspect(capture, expectedSha256, badProfile); }
            catch (IllegalArgumentException expected) { rejected++; continue; }
            throw new IllegalStateException("accepted unsupported profile");
        }
        // Hash integrity cannot substitute for structural/raw-summary validation.
        byte[] bad = capture.clone(); bad[151] = 0;
        int sum = 0;
        for (int i = 0; i < 255; i++) sum += bad[i] & 255;
        bad[255] = (byte) sum;
        try { inspect(bad, digest(bad), PROFILE); }
        catch (IllegalArgumentException expected) {
            System.out.println("PASS: 32 source-model frames; no SI/combined promotion; "
                    + (rejected + 1) + " bad inputs rejected");
            return;
        }
        throw new IllegalStateException("accepted incomplete acquisition with matching hash");
    }

    public static void main(String[] args) throws Exception {
        if (args.length == 3 && args[0].equals("--self-test")) {
            selfTest(Files.readAllBytes(Path.of(args[1])), args[2]);
        } else if (args.length == 4 && args[0].equals("--inspect")) {
            System.out.print(inspect(Files.readAllBytes(Path.of(args[1])), args[2], args[3]));
        } else {
            throw new IllegalArgumentException("--self-test CAPTURE SHA256 | --inspect CAPTURE SHA256 " + PROFILE);
        }
    }
}
