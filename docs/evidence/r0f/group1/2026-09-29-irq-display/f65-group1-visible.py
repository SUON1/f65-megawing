import sys,subprocess
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tools/diagnostics'))
import r0f_group1_negative as n
original=subprocess.Popen
def visible(args,*a,**kw):
 return original([v for v in args if str(v)!='-headless'],*a,**kw)
subprocess.Popen=visible
n.run('nmi-sticky',Path('build/r0f/group1/integration/nmi-visible-01').resolve())
