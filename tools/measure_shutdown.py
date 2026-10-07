"""Replay a client log's latest shutdown timestamps; read-only performance evidence."""
import argparse,datetime,json,re
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('log',type=Path);p.add_argument('--limit',type=float,default=15);a=p.parse_args()
start=None;finish=None;dimensions=0;stalls=[]
for line in a.log.read_text(errors='replace').splitlines():
    stamp=re.match(r'\[([^]]+)\]',line)
    if not stamp:continue
    t=None
    for fmt in ('%d%b%Y %H:%M:%S.%f','%H:%M:%S'):
        try:t=datetime.datetime.strptime(stamp[1],fmt);break
        except ValueError:pass
    if t is None:continue
    if 'Stopping server' in line:start=t;finish=None;dimensions=0
    if start and 'Saving chunks for level' in line:dimensions+=1
    if start and 'All dimensions are saved' in line:finish=t
    if "Can't keep up" in line:
        match=re.search(r'Running (\d+)ms',line)
        if match:stalls.append(int(match[1]))
assert start and finish,'No completed server shutdown captured'
elapsed=(finish-start).total_seconds()
if elapsed<0:elapsed+=86400
print(json.dumps({'shutdown_seconds':elapsed,'dimensions_saved':dimensions,'tick_stalls_ms':stalls,'limit_seconds':a.limit,'passes':elapsed<=a.limit},indent=2))
raise SystemExit(0 if elapsed<=a.limit else 1)
