package f65.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.CRC32;

/** Independent T03 21-stage lineage and result-record oracle. */
public final class R0FSuccessorOracle {
    private static final int PRE_STORAGE_TICKS = 33;
    private static final int POST_STORAGE_TICKS = 33;

    private R0FSuccessorOracle() { }

    private static void require(boolean condition, String message) {
        if (!condition) {
            throw new IllegalArgumentException(message);
        }
    }

    private static int u16(byte[] bytes, int offset) {
        return (bytes[offset] & 255) | ((bytes[offset + 1] & 255) << 8);
    }

    private static long u32(byte[] bytes, int offset) {
        return Integer.toUnsignedLong(u16(bytes, offset)
                                     | (u16(bytes, offset + 2) << 16));
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
            hash = mix(0x0065cf01, tick);
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
        crc.update(bytes, 0, 508);
        return crc.getValue();
    }

    private static void validate(byte[] result) {
        require(result.length == 512, "result length");
        require(result[0] == 'R' && result[1] == 'S'
                && result[2] == 'I' && result[3] == '1', "identity");
        require(result[4] == 1 && result[5] == 127 && result[6] == 0,
                "completion/fault");
        require(result[7] == 9, "lifecycle");
        require(u16(result, 8) == PRE_STORAGE_TICKS, "boundary tick");
        require(u16(result, 10) == PRE_STORAGE_TICKS + POST_STORAGE_TICKS,
                "resumed tick");
        require(u32(result, 12) == golden(PRE_STORAGE_TICKS),
                "boundary checksum");
        require(u32(result, 16)
                == golden(PRE_STORAGE_TICKS + POST_STORAGE_TICKS),
                "continued checksum");
        require(u32(result, 24) != 0 && u32(result, 24) == u32(result, 28),
                "ROM restoration");
        require(u32(result, 32) == u32(result, 36), "reserve sentinel");
        require(u32(result, 40) == u32(result, 44), "low application state");
        require(u32(result, 48) == u32(result, 52), "DOS overlay state");
        require(result[56] == 5 && result[57] == 0 && result[58] == 1,
                "storage transaction");
        require((result[95] & 255) == 31, "resumed service mask");
        require(result[96] == 0, "sticky NMI lockout");
        require(u32(result, 508) == crc(result), "record CRC");
    }

    public static void main(String[] arguments) throws Exception {
        require(golden(PRE_STORAGE_TICKS) == 0xd9eeab81L,
                "CF001 boundary golden");
        if (arguments.length == 1 && arguments[0].equals("--model")) {
            System.out.printf(
                "T03 independent 21-stage lineage PASS: %08X -> %08X%n",
                golden(PRE_STORAGE_TICKS),
                golden(PRE_STORAGE_TICKS + POST_STORAGE_TICKS));
            return;
        }
        require(arguments.length == 1, "usage: --model OR result.bin");
        validate(Files.readAllBytes(Path.of(arguments[0])));
        System.out.println(
            "T03 result/continuation oracle PASS; runtime tier remains external.");
    }
}
