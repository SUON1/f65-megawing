from pathlib import Path
import hashlib,json,re,subprocess
from pypdf import PdfReader
root=Path(__file__).resolve().parents[3]
d=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ids=json.loads((d/'review-identities.json').read_text())
for entry in ids['artifacts']:
 assert sha(d/entry['path'])==entry['sha256'],entry['path']
corpus=json.loads((root/'spec/manifests/spec-corpus.json').read_text())
count=0
for e in corpus['documents']:
 if e.get('present') and e.get('sha256'):
  assert sha(root/e['relative_path'])==e['sha256'],e['relative_path'];count+=1
for p in d.glob('*.md'):
 s=p.read_text()
 assert not re.search(r'[ \t]+$',s,re.M),p.name
 for url in re.findall(r'\]\(([^)]+)\)',s):
  if '://' not in url and not url.startswith('#'):
   assert (p.parent/url.split('#')[0]).exists(),(p.name,url)
for draft,base in ids['full_successors'].items():
 a=(root/base).read_text();b=(d/draft).read_text()
 normalize=lambda s:re.sub(r' {2,}$',r'\\',s,flags=re.M)
 assert normalize(a[a.index('## Appendix A'):])==b[b.index('## Appendix A'):],draft
m=d/'F65_Main_Concept_v1.7_REVIEW_DRAFT.md'
g=(d/'F65_Gameplay_and_Simulation_Supplement_v1.1_REVIEW_DRAFT.md').read_text()
assert '**Proposed parent SHA-256:** `'+sha(m)+'`' in g
s=(d/ids['physics_source']).read_text()
math=re.findall(r'\$\$[\s\S]*?\$\$|(?<!\\)\$[^$\n]+?(?<!\\)\$',s)
assert hashlib.sha256('\n'.join(math).encode()).hexdigest()==ids['inherited_math_sha256']
reader=PdfReader(d/ids['physics_pdf']); text='\n'.join(p.extract_text() for p in reader.pages)
assert len(reader.pages)==40
for term in ['1.3.1','4.4.1','PHY-CONVENTION-01','qualified-pilot','C.3 R1','F.3 External','67dc5c5f25a1ba1488c49a68af3e70ecafe500745aa4f8f29bc004f5920bd0ea']:
 assert term in text,term
assert '\ufffd' not in text
changed=subprocess.check_output(['git','-C',str(root),'diff','--name-only'],text=True).splitlines()
assert changed==['WORK_IN_PROGRESS.md'],changed
subprocess.run(['git','-C',str(root),'diff','--check'],check=True)
for p in d.rglob('*'):
 if p.suffix in {'.md','.json','.py','.cjs'}:
  c=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
  assert c.returncode in (0,1) and not c.stdout and not c.stderr,(p,c.stdout,c.stderr)
print(json.dumps({'package_artifacts':len(ids['artifacts']),'corpus_hashes':count,'inherited_math_expressions':len(math),'pdf_pages':len(reader.pages),'links':'PASS','historical_appendix_content':'PASS','whitespace':'PASS','protected_tracked_files':'UNCHANGED'},indent=2))
