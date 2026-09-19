#!/usr/bin/env python3
"""Verify original PNG label rasters, not a differential image preview."""
import json
from PIL import Image
import r0f_combined_build as cf

cf.current()
path = cf.OUT/'manifests/r0f-d81-release.json'
release = json.loads(path.read_text())
boots = release['XEMU_EVIDENCE']
reference = Image.open(cf.ROOT/boots[1]['directory']/'screen.png').convert('RGB')
rows = (1, 3, 5, 7, 10, 13, 17, 18, 20, 21)
reviews = []
for boot in boots:
    directory = cf.ROOT/boot['directory']
    png = directory/'screen.png'
    if cf.sha(png) != boot['screenshotSha256']:
        raise ValueError('screenshot identity')
    im = Image.open(png).convert('RGB')
    origin = 56 if boot['video'] == '1' else 104
    for row in rows:
        actual = im.crop((80, origin+row*16, 720, origin+row*16+16))
        expected = reference.crop((80, 56+row*16, 720, 56+row*16+16))
        if actual.tobytes() != expected.tobytes():
            raise ValueError(f'constant label raster mismatch: {directory.name} row {row}')
    reviews.append({'directory': boot['directory'], 'screenshotSha256': cf.sha(png),
                    'constantLabelRows': list(rows), 'result': 'PASS'})

diagnostics = []
for name, exit_method, headless in (
    ('xemu-d81-1-1789744642554252000', 'SIGTERM', True),
    ('xemu-d81-1-1789744880280424000', 'UART ~exit', True),
    ('xemu-d81-1-1789745014153785000', 'UART ~exit', False)):
    directory = cf.OUT/name
    evidence_path = directory/'evidence.json'
    evidence = json.loads(evidence_path.read_text())
    if not headless:
        # The probe wrapper removed -headless at Popen. Keep the builder's
        # pre-filter argument list too, rather than misreporting the launch.
        evidence['harnessArgumentsBeforeProbeFilter'] = evidence['command']
        evidence['command'] = [a for a in evidence['command'] if a != '-headless']
    evidence['exitMethod'] = exit_method
    evidence['headless'] = headless
    evidence_path.write_text(json.dumps(evidence, indent=2)+'\n')
    for i in range(3):
        if (directory/f'colors-{i}.bin').read_bytes() != bytes([1])*2000:
            raise ValueError('color memory changed')
        if (directory/f'hud-{i}.bin').read_bytes() != (directory/'hud-0.bin').read_bytes():
            raise ValueError('screen memory changed')
    im = Image.open(directory/'screen.png').convert('RGB')
    for row in rows:
        box = (80, 56+row*16, 720, 56+row*16+16)
        if im.crop(box).tobytes() != reference.crop(box).tobytes():
            raise ValueError('diagnostic screenshot label mismatch')
    diagnostics.append({'directory': str(directory.relative_to(cf.ROOT)), **evidence})

release['VISUAL_REVIEW'] = {
    'result': 'PASS', 'boots': reviews,
    'method': 'Original PNG RGB label rasters match visually reviewed full NTSC reference, with PAL vertical offset; stable text/color RAM corroborates.',
    'previewFinding': 'Apparent missing text in image preview is absent from original PNG pixels; no target defect or artifact change.',
    'diagnosticRuns': diagnostics}
path.write_text(json.dumps(release, indent=2)+'\n')
print('Original PNG raster review PASS: four carrier boots and three diagnostic runs; all constant labels intact.')
