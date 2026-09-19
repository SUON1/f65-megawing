#!/usr/bin/env python3
"""Read-only final-display diagnostics on the exact CF001 carrier."""
import json
import re
import socket
import sys
import time
import r0f_combined_build as cf


def inspect(path, directory):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect(str(path))

        def command(c):
            s.sendall((c + '\r').encode())
            out = b''
            while not out.endswith(b'.\r\n'):
                part = s.recv(8192)
                if not part:
                    raise ValueError('monitor disconnected')
                out += part
            if b'?' in out:
                raise ValueError(repr(out))
            return out.decode()

        def read(at, n):
            out = bytearray()
            for a in range(at, at+n, 256):
                lines = re.findall(r':([0-9A-F]{8}):([0-9A-F]{32})', command('M '+format(a, 'x')))
                if len(lines) != 16:
                    raise ValueError('monitor framing')
                for i, (address, data) in enumerate(lines):
                    if int(address, 16) != a+i*16:
                        raise ValueError('monitor address')
                    out.extend(bytes.fromhex(data))
            return bytes(out[:n])

        records = []
        for i in range(3):
            colors = read(0xff80000, 2000)
            screen = read(0x40000, 2000)
            regs = read(0xffd3000, 256)
            (directory/f'colors-{i}.bin').write_bytes(colors)
            (directory/f'hud-{i}.bin').write_bytes(screen)
            (directory/f'vic-{i}.bin').write_bytes(regs)
            records.append({'colorValues': sorted(set(colors)),
                            'nonWhite': [j for j, v in enumerate(colors) if v != 1],
                            'registers': command('r')})
            time.sleep(1)
        (directory/'visual-probe.json').write_text(json.dumps(records, indent=2)+'\n')
        print(json.dumps(records), flush=True)
        if '--clean-exit' in sys.argv:
            # Exit from Xemu's monitor command loop, not an asynchronous
            # POSIX signal which can interrupt a scanline renderer.
            s.sendall(b'~exit\r')
            while s.recv(8192):
                pass
            time.sleep(1)


if __name__ == '__main__':
    if '--visible' in sys.argv:
        original_popen = cf.subprocess.Popen
        def visible_popen(args, **kwargs):
            return original_popen([a for a in args if a != '-headless'], **kwargs)
        cf.subprocess.Popen = visible_popen
    cf.check_pages = inspect
    cf.xemu('1', True, True)
