import json
from pathlib import Path
root=Path('/tmp/r0f-glyphs')
out=Path('/tmp/r0f-glyphs-reviewed');out.mkdir(exist_ok=True)
for n in range(2,24):
    # Fitted line boundaries for photo 20; other candidates use local boundaries.
    source=Path('/tmp/r0f-glyphs-fit') if n in (5,20) else root
    rows=[list(s) for s in (source/f'{n}-rows.txt').read_text().splitlines()]
    for fix in json.loads(Path('/tmp/r0f-manual-corrections.json').read_text()):
        if fix['photo']==n:
            if 'replacement' in fix:
                rows[fix['row']]=list(fix['replacement'])
            else:
                assert rows[fix['row']][fix['column']]==fix['from']
                rows[fix['row']][fix['column']]=fix['to']
    (out/f'{n}-rows.txt').write_text('\n'.join(''.join(r) for r in rows)+'\n')
