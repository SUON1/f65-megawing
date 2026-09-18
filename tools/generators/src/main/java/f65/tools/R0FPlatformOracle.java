package f65.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.CRC32;

/** Independent observed-result checker, not a SI calibration or workload oracle. */
public final class R0FPlatformOracle {
    private R0FPlatformOracle() { }
    private static long le(byte[] b, int at, int length) {
        long result = 0;
        for (int i = 0; i < length; i++) result |= (b[at + i] & 255L) << (8 * i);
        return result;
    }
    private static void require(boolean value, String why) {
        if (!value) throw new IllegalArgumentException(why);
    }
    private static void validate(byte[] b) {
        require(b.length == 256, "length");
        require(le(b, 0, 4) == 0x31465052L && b[4] == 1, "identity");
        CRC32 crc = new CRC32(); crc.update(b, 0, 252);
        require(crc.getValue() == le(b, 252, 4), "result CRC");
        require(b[6] == 0 && b[5] == 127, "target fault/stage");
        require(b[7] == 2 && b[8] == 1 && (b[9] & 7) == 5 && (b[10] & 0xB9) == 0, "canonical observations");
        require(b[11] == 0 && le(b, 12, 2) >= 32, "IRQ/NMI");
        require(le(b, 14, 2) == 255 && le(b, 168, 2) == 1, "DMA copied bytes/jobs");
        require(le(b, 16, 4) <= 100000, "DMA plausibility, not deadline acceptance");
        require(b[20] > 0 && b[20] <= 8 && b[21] == 1, "real PCM progress/stop");
        require(b[22] == 1 && (b[160] & 255) == 0xA5 && b[161] == 0x5A &&
            (b[162] & 255) == 0xC3 && b[163] == 0x3C && b[164] == 2 &&
            (b[165] & 9) == 0 && (b[166] & 255) == 0x80, "register canaries");
        for (int at = 32; at < 160; at += 4)
            require(le(b, at, 4) > 0 && le(b, at, 4) <= 100000, "frame count observation " + at);
        require(b[25] == 0 && b[26] == 0, "forbidden calibration/combined promotion");
        for (int at : new int[]{27, 167}) require(b[at] == 0, "reserved " + at);
        for (int at = 170; at < 252; at++) require(b[at] == 0, "reserved " + at);
    }
    private static void seal(byte[] b) {
        CRC32 crc = new CRC32(); crc.update(b, 0, 252);
        long v = crc.getValue();
        for (int i = 0; i < 4; i++) b[252 + i] = (byte)(v >> (8 * i));
    }
    private static void reject(byte[] b) {
        boolean rejected = false;
        try { validate(b); } catch (IllegalArgumentException expected) { rejected = true; }
        require(rejected, "mutation incorrectly accepted");
    }
    private static void selfTest(byte[] good) {
        int rejected = 0;
        // Every single-byte corruption must fail the transport checksum.
        for (int at = 0; at < 256; at++) {
            byte[] b = good.clone(); b[at] ^= 1; reject(b); rejected++;
        }
        for (int at : new int[]{0, 4, 5, 6, 7, 8, 9, 11, 14, 21, 22, 25, 26, 27,
                                160, 161, 162, 163, 164, 166, 167, 168, 170, 251}) {
            byte[] b = good.clone(); b[at] ^= 1; seal(b); reject(b); rejected++;
        }
        for (int at = 32; at < 160; at += 4) {
            byte[] b = good.clone();
            for (int i = 0; i < 4; i++) b[at + i] = 0;
            seal(b); reject(b); rejected++;
        }
        for (int at : new int[]{12, 20}) {
            byte[] b = good.clone(); b[at] = 0; b[at + 1] = 0;
            seal(b); reject(b); rejected++;
        }
        reject(java.util.Arrays.copyOf(good, 255));
        reject(java.util.Arrays.copyOf(good, 257));
        System.out.println("PF001 independent oracle negative tests PASS: " + (rejected + 2) + " rejected");
    }
    public static void main(String[] args) throws Exception {
        require(args.length == 1 || (args.length == 2 && args[0].equals("--self-test")), "result path or --self-test result path required");
        byte[] b = Files.readAllBytes(Path.of(args[args.length - 1]));
        require(b.length == 256, "length");
        System.out.printf("Observed: stage=%02X fault=%02X B=%02X SPH=%02X port=%02X D030=%02X IRQ=%d DMA=%d PCM=%d%n",
            b[5], b[6], b[7], b[8], b[9], b[10], le(b, 12, 2), le(b, 14, 2), le(b, 20, 1));
        validate(b);
        if (args.length == 2) selfTest(b);
        System.out.println("PF001 platform observations PASS; calibration=false fullCombined=false physical=NOT_RUN");
    }
}
