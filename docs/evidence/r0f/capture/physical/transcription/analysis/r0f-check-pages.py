from pathlib import Path
import zlib,json,os
root=Path(os.environ.get('R0F_GLYPH_OUT','/tmp/r0f-glyphs'))
crcs=['1947E857','7ED96198','F76254EE','29F01800','8EFCD67E','6076FED9','1120103D','603A6B13','D86B6DCC','65802B88','22DD7E39','0A2873D3','2E61532C','1BECED22','AD3287BF','8ADA5789','ED9D3432','05A27ED7','726262F9','DFDD7431','CEC53C4A','0D39992D']
total=bytearray();report=[]
for n,expected in enumerate(crcs,2):
    rows=(root/f'{n}-rows.txt').read_text().splitlines()
    data=b''.join(bytes.fromhex(r.split(':')[1]) for r in rows)
    if n==23:data=data[:384]
    actual=f'{zlib.crc32(data):08X}'
    report.append(dict(photo=n,page=n-1,expected=expected,actual=actual,match=actual==expected))
    print(n,expected,actual,'PASS' if actual==expected else 'MISMATCH')
    total.extend(data)
print('FULL',f'{zlib.crc32(total):08X}','EXPECTED 8D78FBC0')
(root/'crc-assessment.json').write_text(json.dumps(report,indent=2)+'\n')
