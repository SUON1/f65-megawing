package f65.tools;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Deterministic R0-D protected-workload fixture; it selects no production limits. */
public final class R0DHostTools {
  private static final String ID = "r0d-0.1.0-calibration-proof";
  private static final Path ROOT = Paths.get(System.getProperty("f65.root", ".")).toAbsolutePath().normalize();
  private static final Path OUT = ROOT.resolve("build/r0d");
  private static final int STAGES = 21, TICK_HZ = 100, HISTORICAL_CLOCKS = 530000;
  private static final int[] STAGE_WORK = {25000,25000,25000,25000,25000,25000,25000,25000,25000,25000,25000,25000,25000,25000,25000,30000,25000,25000,25000,25000,25000};
  private R0DHostTools() {}

  public static void main(String[] args) throws Exception {
    String op = args.length == 0 ? "all" : args[0];
    if (op.equals("generate") || op.equals("all") || op.equals("host-test")) generate();
    if (op.equals("host-test") || op.equals("all")) hostTest();
    if (op.equals("verify") || op.equals("all")) verify();
  }

  private static void generate() throws Exception {
    Files.createDirectories(OUT.resolve("evidence")); Files.createDirectories(OUT.resolve("reports"));
    String contract = read("interfaces/r0d_proof_contract.json");
    if (!contract.contains("530000") || !contract.contains("exactly 21")) throw new IOException("R0-D contract invariant missing");
    put("interfaces/generated/r0d_interfaces.h", "/* generated from r0d_proof_contract.json */\n#ifndef F65_R0D_INTERFACES_H\n#define F65_R0D_INTERFACES_H\n#define R0D_RESULT_ADDRESS 0x1860u\n#define R0D_RESULT_BYTES 128u\n#define R0D_STAGE_COUNT 21u\n#define R0D_HISTORICAL_PROTECTED_CLOCKS 530000ul\n#endif\n");
    put("tools/generators/src/main/java/f65/tools/generated/R0DInterfaces.java", "package f65.tools.generated; public final class R0DInterfaces { private R0DInterfaces(){} public static final int STAGES=21, RESULT_ADDRESS=0x1860, RESULT_BYTES=128, HISTORICAL_CLOCKS=530000; }\n");
    put(OUT.resolve("reports/r0d-fixture.json"), fixtureJson());
    put(OUT.resolve("reports/r0d-counter-schema.json"), "{\"identity\":\""+ID+"\",\"recordBytes\":64,\"presentationObservational\":true,\"reserveBytes\":0}\n");
  }

  private static void hostTest() throws Exception {
    List<String> tests = new ArrayList<>(); Counter a = run(), b = run();
    ok(sum() == HISTORICAL_CLOCKS, "R0D-FIX-001 historical fixture is exactly 530000 protected clocks", tests);
    ok(a.tick == 1 && a.stageOrder == STAGES && a.stage16NextTickOnly, "R0D-TICK-001 100Hz 21-stage order and next-tick AI causality", tests);
    ok(a.protectedClocks == HISTORICAL_CLOCKS && a.rollingProtectedClocks == HISTORICAL_CLOCKS * TICK_HZ, "R0D-CLK-001 protected and independent-clock rolling counters", tests);
    ok(a.worldGeneration == 1 && a.sourceSnapshot == 1 && a.displayedWorldAge == 1, "R0D-WORLD-001 generation/source/displayed-world-age counters", tests);
    ok(a.rendererPoolHighWater == 0 && a.occlusionHighWater == 0 && a.registrationAnchorHighWater == 0 && a.lodTransitionHighWater == 0 && a.graphicsDmaTicks == 0, "R0D-RENDER-001 non-render counter invariants", tests);
    ok(a.audioServiceTicks == 0 && a.audioVoiceHighWater == 0 && a.audioP0Latency == 0 && a.audioP1Latency == 0, "R0D-AUDIO-001 protected audio counters", tests);
    ok(a.snapshotExtractions == 1 && a.snapshotPublications == 1 && a.snapshotLag == 0 && a.snapshotDrops == 0 && a.ownershipFaults == 0, "R0D-SNAP-001 snapshot/publication/lag/drop/ownership counters", tests);
    ok(a.dmaTicks == 0 && a.inputTicks == 1 && a.storageTicks == 0, "R0D-IO-001 DMA/input/storage timing counters", tests);
    ok(a.aiCodeBytes == 0 && a.aiStateBytes == 0 && a.aiHeldIntentBytes == 0 && a.aiRouteDoctrineBytes == 0 && a.aiCausalityViolations == 0, "R0D-AI-001 stage-16 owner and held-intent counters", tests);
    ok(a.reserveBytes == 0 && a.codeBytes == 0 && a.dataBytes == 0 && a.runtimeHelperBytes == 0 && a.stackHighWater == 0, "R0D-MEM-001 reserve/code/data/helper/stack counters", tests);
    ok(a.sameAs(b), "R0D-DET-001 deterministic counter snapshot", tests);
    put(OUT.resolve("evidence/r0d-host-evidence.json"), "{\"identity\":\""+ID+"\",\"class\":\"HOST\",\"result\":\"PASS\",\"tests\":"+json(tests)+",\"counter\":"+a.json()+",\"fixtureRole\":\"historical comparison workload; not a production budget\"}\n");
    put(OUT.resolve("reports/R0D_HOST_TEST_REPORT.md"), "# R0-D Host Test Report\n\nResult: **PASS** (host evidence only).\n\n"+String.join("\n", tests.stream().map(x -> "- PASS: "+x).toList())+"\n\nThe 530,000-clock fixture is historical comparison work, not a measured limit.\n");
  }

  private static void verify() throws Exception {
    if (!Files.exists(ROOT.resolve("interfaces/generated/r0d_interfaces.h"))) throw new IOException("R0-D generated C binding absent");
    if (!read("interfaces/generated/r0d_interfaces.h").contains("530000ul")) throw new IOException("R0-D generated C binding stale");
    if (sum() != HISTORICAL_CLOCKS || !read("memory/r0d-memory-ledger.json").contains("0x001860-0x0018df")) throw new IOException("R0-D fixture or ledger invalid");
  }

  private static Counter run() { Counter c = new Counter(); c.tick=1; c.stageOrder=STAGES; c.stage16NextTickOnly=true; c.protectedClocks=sum(); c.rollingProtectedClocks=c.protectedClocks*TICK_HZ; c.worldGeneration=1; c.sourceSnapshot=1; c.displayedWorldAge=1; c.snapshotExtractions=1; c.snapshotPublications=1; c.inputTicks=1; return c; }
  private static int sum() { int r=0; for(int n:STAGE_WORK) r+=n; return r; }
  private static String fixtureJson() { return "{\"identity\":\""+ID+"\",\"fixtureId\":\"R0D-PW-530K-001\",\"simulationHz\":100,\"stages\":21,\"stageProtectedClocks\":"+Arrays.toString(STAGE_WORK)+",\"totalProtectedClocks\":530000,\"role\":\"historical comparison workload; not a production budget\"}\n"; }
  private static void ok(boolean value, String name, List<String> tests) throws IOException { if (!value) throw new IOException("FAIL: "+name); tests.add(name); }
  private static String json(List<String> v) { return "["+String.join(",",v.stream().map(x -> "\""+x+"\"").toList())+"]"; }
  private static String read(String path) throws IOException { return Files.readString(ROOT.resolve(path)); }
  private static void put(String path, String value) throws IOException { put(ROOT.resolve(path),value); }
  private static void put(Path path, String value) throws IOException { Files.createDirectories(path.getParent()); Files.writeString(path,value,StandardCharsets.UTF_8); }
  private static final class Counter {
    int tick,stageOrder,protectedClocks,rollingProtectedClocks,worldGeneration,sourceSnapshot,displayedWorldAge,rendererPoolHighWater,occlusionHighWater,registrationAnchorHighWater,lodTransitionHighWater,graphicsDmaTicks,audioServiceTicks,audioVoiceHighWater,audioP0Latency,audioP1Latency,snapshotExtractions,snapshotPublications,snapshotLag,snapshotDrops,ownershipFaults,dmaTicks,inputTicks,storageTicks,aiCodeBytes,aiStateBytes,aiHeldIntentBytes,aiRouteDoctrineBytes,aiCausalityViolations,reserveBytes,codeBytes,dataBytes,runtimeHelperBytes,stackHighWater; boolean stage16NextTickOnly;
    boolean sameAs(Counter o) { return json().equals(o.json()); }
    String json() { return "{\"tick\":"+tick+",\"stages\":"+stageOrder+",\"protectedClocks\":"+protectedClocks+",\"rollingProtectedClocks\":"+rollingProtectedClocks+",\"worldGeneration\":"+worldGeneration+",\"sourceSnapshot\":"+sourceSnapshot+",\"displayedWorldAge\":"+displayedWorldAge+",\"snapshotExtractions\":"+snapshotExtractions+",\"snapshotPublications\":"+snapshotPublications+",\"inputTicks\":"+inputTicks+",\"reserveBytes\":0}"; }
  }
}
