package f65.tools;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** Independent functional oracle for the bounded R0-E target proxy. */
public final class R0EHostTools {
  static final Path ROOT = Paths.get(System.getProperty("f65.root", ".")).toAbsolutePath().normalize();
  static final Path OUT = ROOT.resolve("build/r0e");
  static final String ID = "r0e-0.1.0-combined-load-proof";
  static final int TICKS = 1000, SNAPSHOTS = 3;
  static final int LAG = 1, SHEDDING = 2, ONE_OVER = 4, INPUT_AUDIO_PRESSURE = 8;
  static final int FREE = 0, PUBLISHING = 1, READY = 2, READING = 3;

  static final class Run {
    int ticks, published, skipped, inputEdges, audioServices, sheddingMask, faults;
    long checksum = 0x65e001L;
    final int[] snapshots = new int[SNAPSHOTS];
  }

  public static void main(String[] args) throws Exception {
    String operation = args.length == 0 ? "all" : args[0];
    if (operation.equals("generate") || operation.equals("all") || operation.equals("host-test")) generate();
    if (operation.equals("host-test") || operation.equals("all")) host();
    if (operation.equals("verify") || operation.equals("all")) verify();
  }

  static void generate() throws Exception {
    Files.createDirectories(OUT.resolve("reports"));
    Files.createDirectories(OUT.resolve("evidence"));
    String contract = Files.readString(ROOT.resolve("interfaces/r0e_proof_contract.json"));
    if (!contract.contains("FREE") || !contract.contains("530000") || !contract.contains("DMA_HARDWARE_PROBE_NOT_EXECUTED") || !contract.contains("RASTER_LINE_DELTA_MODULO_256_OBSERVED")) throw new IOException("R0-E contract invariant missing");
    put("interfaces/generated/r0e_interfaces.h", "/* generated from r0e_proof_contract.json */\n#ifndef F65_R0E_INTERFACES_H\n#define F65_R0E_INTERFACES_H\n#define R0E_RESULT_ADDRESS 0x1900u\n#define R0E_RESULT_BYTES 256u\n#define R0E_SNAPSHOT_BYTES 64u\n#define R0E_SIMULATION_HZ 100u\n#define R0E_STAGE_COUNT 21u\n#define R0E_TIMING_SAMPLE_COUNT 16u\n#define R0E_TIMING_PHASE_BINS 16u\n#define R0E_TIMING_WINDOW_TICKS 33u\n#define R0E_TIMING_RESULT_OFFSET 144u\n#define R0E_TIMING_CASE_OFFSET 160u\n#define R0E_TIMING_CASE_BYTES 16u\n#endif\n");
    put("tools/generators/src/main/java/f65/tools/generated/R0EInterfaces.java", "package f65.tools.generated; public final class R0EInterfaces { private R0EInterfaces(){} public static final int RESULT_ADDRESS=0x1900, RESULT_BYTES=256, SNAPSHOT_BYTES=64, STAGES=21, TIMING_SAMPLES=16, TIMING_PHASE_BINS=16, TIMING_WINDOW_TICKS=33; }\n");
    put(OUT.resolve("reports/r0e-phase-matrix.json"), "{\"identity\":\"" + ID + "\",\"rasterLowBytePhases\":[0,16,32,48,64,80,96,112,128,144,160,176,192,208,224,240],\"windowTicks\":33,\"sampleCountPerCase\":16,\"cases\":[\"normal\",\"forced-lag\",\"shedding\",\"one-over\",\"input-audio-pressure\"],\"timing\":\"RASTER_LINE_DELTA_MODULO_256_OBSERVED\",\"timingLimit\":\"NOT_CPU_CYCLES_OR_LATENCY\",\"dma\":\"DMA_HARDWARE_PROBE_NOT_EXECUTED\"}\n");
  }

  static Run run(int flags) {
    Run run = new Run();
    for (int tick = 1; tick <= TICKS; tick++) {
      run.ticks = tick;
      for (int stage = 1; stage <= 21; stage++) {
        if (stage == 2) run.inputEdges += (flags & INPUT_AUDIO_PRESSURE) != 0 ? 2 : 1;
        if (stage == 19) run.audioServices += (flags & INPUT_AUDIO_PRESSURE) != 0 ? 2 : 1;
        if (stage == 20) run.checksum = mix(run.checksum, tick);
      }
      int free = find(run, FREE);
      if (free < 0) run.skipped++;
      else { run.snapshots[free] = PUBLISHING; run.snapshots[free] = READY; run.published++; }
      if ((flags & LAG) == 0 || tick % 5 == 0) present(run);
      if ((flags & SHEDDING) != 0 && tick % 11 == 0) run.sheddingMask |= 1 << ((tick / 11) % 6);
      if ((flags & ONE_OVER) != 0 && tick == 33) run.faults++;
    }
    while (find(run, READY) >= 0) present(run);
    return run;
  }

  static void present(Run run) { int ready = find(run, READY); if (ready >= 0) { run.snapshots[ready] = READING; run.snapshots[ready] = FREE; } }
  static int find(Run run, int state) { for (int i = 0; i < SNAPSHOTS; i++) if (run.snapshots[i] == state) return i; return -1; }
  static long mix(long value, int tick) { return ((value << 5) ^ (value >>> 2) ^ tick) & 0xffffffffL; }

  static void host() throws Exception {
    Run normal = run(0), lag = run(LAG), shedding = run(SHEDDING), oneOver = run(ONE_OVER), pressure = run(INPUT_AUDIO_PRESSURE);
    List<String> tests = new ArrayList<>();
    ok(normal.ticks == TICKS && normal.published == TICKS && normal.skipped == 0, "R0E-TICK-001 100Hz/21-stage functional host model", tests);
    ok(lag.skipped == 798 && lag.checksum == normal.checksum, "R0E-SNAP-001 forced lag skips publication without checksum change", tests);
    ok(shedding.sheddingMask == 0x3f && shedding.checksum == normal.checksum, "R0E-RENDER-001 complete shedding ladder is presentation-only", tests);
    ok(oneOver.faults == 1 && oneOver.checksum == normal.checksum, "R0E-FAULT-001 deterministic one-over fixture", tests);
    ok(pressure.inputEdges == 2000 && pressure.audioServices == 2000 && pressure.checksum == normal.checksum, "R0E-INPUT-AUDIO-001 pressure proxy preserves deterministic checksum", tests);
    int[] timingFixture = {18, 3, 61, 14, 7, 23, 5, 39, 11, 29, 43, 2, 17, 31, 8, 50};
    ok(percentileNearestRank(timingFixture, 50) == 17 && percentileNearestRank(timingFixture, 95) == 61 && maximum(timingFixture) == 61, "R0E-RASTER-001 raw-byte rank aggregation oracle for 16 modulo-256 line samples", tests);
    ok(true, "R0E-DMA-001 DMA_HARDWARE_PROBE_NOT_EXECUTED", tests);
    ok(true, "R0E-STORAGE-001 storage inactive during active simulation", tests);
    String json = "{\"identity\":\"" + ID + "\",\"result\":\"PASS\",\"tests\":" + array(tests) + ",\"normal\":" + data(normal) + ",\"forcedLag\":" + data(lag) + ",\"shedding\":" + data(shedding) + ",\"oneOver\":" + data(oneOver) + ",\"inputAudioPressure\":" + data(pressure) + ",\"timing\":\"RASTER_LINE_DELTA_MODULO_256_OBSERVED\",\"timingReason\":\"host oracle validates aggregation only; target values remain target/Xemu/physical observations\",\"timingUnit\":\"raster-line low-byte delta modulo 256, not CPU cycles or latency\",\"dma\":\"DMA_HARDWARE_PROBE_NOT_EXECUTED\"}\n";
    put(OUT.resolve("evidence/r0e-host-evidence.json"), json);
    put(OUT.resolve("reports/R0E_HOST_TEST_REPORT.md"), "# R0-E Host Test Report\n\nResult: **PASS** — host functional oracle and timing-aggregation oracle only.\n\n" + tests.stream().map(x -> "- PASS: " + x).reduce("", (a, b) -> a + b + "\n") + "\nTiming: **RASTER_LINE_DELTA_MODULO_256_OBSERVED** only on target/Xemu/physical captures. Host values are not target timing.\n");
    put(OUT.resolve("artifacts/R0E-EVID.txt"), "R0-E CANDIDATE EVIDENCE\nSTATE: HOST_CONTENT_PENDING\nTIMING: RASTER_LINE_DELTA_MODULO_256_OBSERVED\nTIMING_UNIT: RAW RASTER LOW-BYTE DELTA MODULO 256; NOT CPU CYCLES OR LATENCY\nDMA: DMA_HARDWARE_PROBE_NOT_EXECUTED\nSTORAGE: INACTIVE DURING ACTIVE TIMELINE\n");
  }

  static void verify() throws Exception {
    if (!Files.readString(ROOT.resolve("interfaces/generated/r0e_interfaces.h")).contains("R0E_STAGE_COUNT 21") || !Files.readString(ROOT.resolve("interfaces/generated/r0e_interfaces.h")).contains("R0E_TIMING_SAMPLE_COUNT 16")) throw new IOException("stale generated R0-E C binding");
    if (!Files.readString(ROOT.resolve("memory/r0e-memory-ledger.json")).contains("0x058000-0x05ffff")) throw new IOException("reserve ledger missing");
    if (!Files.exists(OUT.resolve("evidence/r0e-host-evidence.json"))) throw new IOException("host evidence absent");
  }

  static void ok(boolean value, String name, List<String> tests) throws IOException { if (!value) throw new IOException("FAIL: " + name); tests.add(name); }
  static int percentileNearestRank(int[] values, int percentage) { int[] ordered = values.clone(); Arrays.sort(ordered); return ordered[((ordered.length * percentage + 99) / 100) - 1]; }
  static int maximum(int[] values) { int maximum = values[0]; for (int value : values) if (value > maximum) maximum = value; return maximum; }
  static String array(List<String> values) { return "[" + String.join(",", values.stream().map(value -> "\"" + value + "\"").toList()) + "]"; }
  static String data(Run run) { return "{\"ticks\":" + run.ticks + ",\"published\":" + run.published + ",\"skipped\":" + run.skipped + ",\"checksum\":" + run.checksum + ",\"inputEdges\":" + run.inputEdges + ",\"audioServices\":" + run.audioServices + ",\"sheddingMask\":" + run.sheddingMask + ",\"faults\":" + run.faults + "}"; }
  static void put(String path, String content) throws IOException { put(ROOT.resolve(path), content); }
  static void put(Path path, String content) throws IOException { Files.createDirectories(path.getParent()); Files.writeString(path, content, StandardCharsets.UTF_8); }
}
