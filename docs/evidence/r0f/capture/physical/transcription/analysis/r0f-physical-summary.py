"""Summarize already Java-validated bytes without assigning physical time units."""
import hashlib,json,struct,zlib
from pathlib import Path
root=Path('/Users/slice/Documents/ChatGPT/F65 Megawing')
e=root/'docs/evidence/r0f/capture/physical'
b=(e/'physical-capture.bin').read_bytes()
u16=lambda at:struct.unpack_from('<H',b,at)[0]
u32=lambda at:struct.unpack_from('<I',b,at)[0]
cases=[]
for c,name in enumerate(['NORMAL','LAG','SHED','FAULT','PRESS']):
    durations=[u16(256+(c*528+i)*4) for i in range(528)]
    late=[u16(258+(c*528+i)*4) for i in range(528)]
    spans=[u32(256+5*528*4+(c*16+i)*4) for i in range(16)]
    ordered=sorted(durations)
    cases.append(dict(case=name,samples=len(durations),p50=ordered[263],p95=ordered[501],maximum=ordered[-1],maximumLateness=max(late),misses=sum(v!=0 for v in late),phaseMaskHex=f'{u16(170+c*16):04X}',maximumSpan33=max(spans)))
result=dict(status='PHYSICAL_CAPTURE_TRANSPORT_AND_INDEPENDENT_RAW_REDUCTION_PASS',
    units='RAW_CIA_COUNTS_NOT_CALIBRATED_TIME',captureBytes=len(b),captureSha256=hashlib.sha256(b).hexdigest(),streamCrc32=f'{zlib.crc32(b):08X}',pageCrcCount=22,
    samples=2640,cohortSpans=80,cases=cases,frameCountsBefore=u32(152),frameCountsAfter=u32(240),
    summaryCorruptionsRejected=35,fixedFieldCorruptionsRejected=163,
    validators=[dict(path=str(p.relative_to(root)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [root/'tools/generators/src/main/java/f65/tools/R0FCapturePages.java',root/'tools/generators/src/main/java/f65/tools/R0FTimingOracle.java']],
    evidence=['physical-capture.java.txt','physical-timing.java.txt','transcription/transcription-manifest.json','TRANSFER-TERMINAL.txt'],
    sdHashExtentEject='PASS',fullR0FAcceptance='NOT_GRANTED',calibration='NOT_PERFORMED',fullCombinedServices='NOT_IMPLEMENTED',source='Owner photos; image-only transcription and explicitly recorded visual corrections. No emulator bytes or expected measurement values substituted.')
with (e/'physical-validation.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
