package f65.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.CRC32;

/** Independent T04 successor result and SAVE-payload oracle. */
public final class R0FSuccessorRuntimeOracle {
    private static final int RESULT_BYTES = 512;
    private static final int RESULT_CRC_OFFSET = 508;
    private static final int PRE_STORAGE_TICKS = 33;
    private static final int POST_STORAGE_TICKS = 33;
    private static final int STORAGE_PAYLOAD_ADDRESS = 0x29C4;
    private static final int STORAGE_PAYLOAD_BYTES = 32;

    private R0FSuccessorRuntimeOracle() {
    }

    private static void require(boolean condition, String message) {
        if (!condition) {
            throw new IllegalStateException(message);
        }
    }

    private static int u16(byte[] bytes, int offset) {
        return (bytes[offset] & 0xFF) | ((bytes[offset + 1] & 0xFF) << 8);
    }

    private static long u32(byte[] bytes, int offset) {
        return Integer.toUnsignedLong(
            (bytes[offset] & 0xFF)
                | ((bytes[offset + 1] & 0xFF) << 8)
                | ((bytes[offset + 2] & 0xFF) << 16)
                | ((bytes[offset + 3] & 0xFF) << 24));
    }

    private static int mix(int hash, int value) {
        return Integer.rotateLeft(hash, 5) ^ value;
    }

    private static long golden(int ticks) {
        int[] x = new int[123];
        int[] y = new int[123];
        int[] z = new int[123];
        int[] command = new int[9];
        int[] next = new int[9];
        int[] table = {3, 7, 2, 11, 5, 13, 1, 9,
                       4, 15, 6, 12, 8, 14, 10, 0};
        int hash = 0;

        for (int index = 0; index < 123; index++) {
            x[index] = index * 17 + 3;
            y[index] = index * 13 + 5;
            z[index] = index * 7 + 257;
        }
        for (int tick = 1; tick <= ticks; tick++) {
            System.arraycopy(next, 0, command, 0, command.length);
            int environment = (tick & 7) + table[tick & 15];

            for (int stage = 5; stage <= 10; stage++) {
                for (int index = 0; index < 9; index++) {
                    int value = (x[index] + command[index]
                                 + environment + stage) & 65535;
                    x[index] = value ^ (y[index] >>> 3);
                    y[index] = (y[index] + table[value & 15]) & 65535;
                    z[index] = 257 + ((z[index] + index + stage) & 1023);
                }
            }
            for (int index = 9; index < 97; index++) {
                x[index] = (x[index] + table[(index + tick) & 15]) & 65535;
                y[index] ^= x[index] >>> 2;
                z[index] = 257 + ((z[index] + 3) & 1023);
            }
            for (int index = 0; index < 9; index++) {
                y[index] = (y[index] + (index == 0 ? 8 : 7)) & 65535;
            }
            for (int index = 113; index < 123; index++) {
                x[index] = (x[index] + x[(index - 113) % 9]) & 65535;
                y[index] ^= tick;
            }
            for (int index = 0; index < 9; index++) {
                next[index] = (x[113 + index] ^ tick) & 15;
            }
            for (int index = 97; index < 113; index++) {
                x[index] = (x[index] + environment + 1) & 65535;
            }
            hash = mix(0x0065CF01, tick);
            for (int index = 0; index < 123; index++) {
                hash = mix(hash, x[index]);
                hash = mix(hash, y[index]);
                hash = mix(hash, z[index]);
            }
            for (int index = 0; index < 9; index++) {
                hash = mix(hash, command[index]);
                hash = mix(hash, next[index]);
            }
        }
        return Integer.toUnsignedLong(hash);
    }

    private static long crc(byte[] bytes) {
        CRC32 crc = new CRC32();

        crc.update(bytes, 0, RESULT_CRC_OFFSET);
        return crc.getValue();
    }

    private static void validateResult(byte[] result) {
        require(result.length == RESULT_BYTES, "result length");
        require(result[0] == 'R' && result[1] == 'S'
                && result[2] == 'I' && result[3] == '1', "identity");
        require((result[4] & 0xFF) == 1, "version");
        require((result[5] & 0xFF) == 127, "completion stage");
        require((result[6] & 0xFF) == 0, "fault");
        require((result[7] & 0xFF) == 9, "lifecycle");
        require(u16(result, 8) == PRE_STORAGE_TICKS, "boundary tick");
        require(u16(result, 10) == PRE_STORAGE_TICKS + POST_STORAGE_TICKS,
                "continued tick");
        require(u32(result, 12) == golden(PRE_STORAGE_TICKS),
                "boundary checksum");
        require(u32(result, 16)
                == golden(PRE_STORAGE_TICKS + POST_STORAGE_TICKS),
                "continued checksum");
        require(u32(result, 20) != 0, "KERNAL context CRC");
        require(u32(result, 24) != 0
                && u32(result, 24) == u32(result, 28),
                "ROM restoration");
        require(u32(result, 32) == u32(result, 36), "reserve sentinel");
        require(u32(result, 40) == u32(result, 44),
                "low application restoration");
        require(u32(result, 48) == u32(result, 52),
                "DOS overlay restoration");
        require((result[56] & 0xFF) == 5
                && (result[57] & 0xFF) == 0
                && (result[58] & 0xFF) == 1
                && (result[59] & 0xFF) == 0,
                "storage transaction");
        require((result[92] & 0xFF) == 2, "canonical base page");
        require((result[93] & 0xFF) == 0x35, "canonical CPU port");
        require((result[94] & 0xFF) == 1, "context invalidation");
        require((result[95] & 0xFF) == 31, "resumed service mask");
        require((result[96] & 0xFF) == 0, "sticky NMI");
        require(u32(result, RESULT_CRC_OFFSET) == crc(result),
                "result CRC");
    }

    private static void validateSave(byte[] result, byte[] saved) {
        require(saved.length == STORAGE_PAYLOAD_BYTES + 2, "SAVE length");
        require(u16(saved, 0) == STORAGE_PAYLOAD_ADDRESS,
                "SAVE load address");
        long checksum = u32(result, 12);

        for (int index = 0; index < STORAGE_PAYLOAD_BYTES; index++) {
            int checksumByte = (int) ((checksum >> ((index & 3) * 8)) & 0xFF);
            int expected = checksumByte ^ index;

            require((saved[index + 2] & 0xFF) == expected,
                    "SAVE payload byte " + index);
        }
    }

    public static void main(String[] arguments) throws Exception {
        require(golden(PRE_STORAGE_TICKS) == 0xD9EEAB81L,
                "boundary golden");
        require(golden(PRE_STORAGE_TICKS + POST_STORAGE_TICKS) == 0x307A70D6L,
                "continued golden");
        if (arguments.length == 1 && arguments[0].equals("--model")) {
            System.out.println(
                "T04 independent lineage PASS: D9EEAB81 -> 307A70D6");
            return;
        }
        require(arguments.length == 2, "usage: result.bin saved.prg");
        byte[] result = Files.readAllBytes(Path.of(arguments[0]));
        byte[] saved = Files.readAllBytes(Path.of(arguments[1]));

        validateResult(result);
        validateSave(result, saved);
        System.out.println(
            "T04 independent result/SAVE oracle PASS: D9EEAB81 -> 307A70D6");
    }
}
