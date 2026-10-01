#!/usr/bin/env python3
"""CAP13 viewer test on a fresh exact-name disposable Xemu carrier copy.

MANDATORY D81 LOADABILITY GATE: read 00_D81_LOADABILITY_GATE.md before use.
Never mounts the canonical writable. Only virtual keys, not code/result writes.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import socket
import subprocess
import tempfile
import time

from r0f_successor_capture import parse_rows
import r0f_successor_emulator as runtime


def inspect(sockpath, directory):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(5)
        connection.connect(str(sockpath))

        def command(text):
            connection.sendall((text + '\r').encode())
            output = b''
            while not output.endswith(b'.\r\n'):
                chunk = connection.recv(8192)
                if not chunk:
                    raise ValueError('monitor disconnected')
                output += chunk
            if b'?' in output:
                raise ValueError('monitor rejected command')
            return output.decode()

        def read(address, length):
            output = bytearray()
            for base in range(address, address + length, 256):
                rows = re.findall(r':([0-9A-F]{8}):([0-9A-F]{32})',
                                  command(f'M {base:x}'))
                if len(rows) != 16:
                    raise ValueError('monitor framing')
                for index, (actual, data) in enumerate(rows):
                    if int(actual, 16) != base + index * 16:
                        raise ValueError('monitor address')
                    output.extend(bytes.fromhex(data))
            return bytes(output[:length])

        def key(code):
            command(f's ffd3615 {code:x}')
            time.sleep(0.10)
            command('s ffd3615 7f')
            time.sleep(0.75)

        result = read(0x1900, 512)
        runtime.validate_success_result(result)
        summary = read(0x40000, 2000)
        transcript = []
        pages = []
        for page in range(2):
            key(39)  # N, pinned Xemu matrix index; inherited CF001 test route.
            raw = read(0x40000, 2000)
            pages.append(raw)
            text = ''.join(chr(c + 64) if 1 <= c <= 26 else chr(c) for c in raw)
            lines = [text[index:index + 80] for index in range(0, 2000, 80)]
            (directory / f'page-{page + 1}.txt').write_text('\n'.join(lines) + '\n')
            if lines[3][5:7] != f'{page + 1:02X}':
                raise ValueError('page header')
            if lines[3][30:].strip():
                raise ValueError('stale heading text')
            for row in lines[5:21]:
                transcript.append(row[:4] + ' ' + row[6:53].strip())
        imported = parse_rows('\n'.join(transcript))
        if imported != result:
            raise ValueError('screen differs from result')
        key(39)
        if read(0x40000, 2000) != pages[0]:
            raise ValueError('page wrap')
        key(13)  # S.
        if read(0x40000, 2000) != summary or read(0x1900, 512) != result:
            raise ValueError('summary or result changed')
        key(39)
        if read(0x40000, 2000) != pages[0]:
            raise ValueError('summary did not reset page navigation')
        (directory / 'transcript.txt').write_text('\n'.join(transcript) + '\n')
        (directory / 'result.bin').write_bytes(result)
        connection.sendall(b'~exit\r')
        while connection.recv(8192):
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    directory = args.out.resolve()
    directory.mkdir(parents=True, exist_ok=False)
    source = runtime.ROOT / 'build/r0f/d81-workflow/R0FCAP13/canonical/R0FCAP13.D81'
    gate = json.loads((source.parent / 'host-gate.json').read_text())
    digest = runtime.sha256(source)
    if gate['D81_SHA256'] != digest or gate['HOST_CONTENT_RESULT'] != 'PASS':
        raise ValueError('canonical host gate')
    runtime.pin_runtime_tools()
    image = directory / source.name
    shutil.copyfile(source, image)
    if runtime.sha256(image) != digest:
        raise ValueError('copy mismatch')
    sd = directory / 'disposable-sd.img'
    subprocess.run(['/bin/cp', '-c', str(runtime.XEMU_SD), str(sd)], check=True)
    with tempfile.TemporaryDirectory(prefix='cap13-') as temporary:
        sockpath = Path(temporary) / 'mon'
        command = [runtime.ROOT / 'toolchain/xemu/xmega65', '-skipconfigfile',
                   '-headless', '-fastboot', '-videostd', '1', '-fastclock', '40.5',
                   '-rom', runtime.ROM, '-sdimg', sd, '-8', image, '-autoload',
                   '-uartmon', sockpath, '-screenshot', directory / 'page-1.png']
        with (directory / 'xemu.log').open('wb') as log:
            process = subprocess.Popen(list(map(str, command)), stdout=log,
                                       stderr=subprocess.STDOUT)
            try:
                time.sleep(80)
                inspect(sockpath, directory)
                process.wait(timeout=10)
            finally:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=10)
    if runtime.sha256(source) != digest:
        raise ValueError('canonical changed')
    (directory / 'viewer.json').write_text(json.dumps({
        'result': 'PASS', 'tier': 'XEMU_VIEWER_NOT_PHYSICAL',
        'canonicalSha256': digest, 'postRunSha256': runtime.sha256(image),
        'checks': ['512 displayed bytes', 'CRC and semantic importer',
                   'page wrap', 'summary return', 'summary resets navigation',
                   'immutable result'],
        'command': list(map(str, command)),
    }, indent=2) + '\n')
    print('CAP13 exact-copy viewer PASS')


if __name__ == '__main__':
    main()
