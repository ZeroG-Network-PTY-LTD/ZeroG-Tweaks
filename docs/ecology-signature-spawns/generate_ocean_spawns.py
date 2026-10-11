"""Regular Tidewraith ocean habitat; never naturally spawn the approved boss."""
import argparse
import json
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--check',action='store_true')
a=p.parse_args()
data={'type':'neoforge:add_spawns','biomes':['zerog_tweaks:wasteland_'+name for name in
      ['deep_trenches','kelp_jungles','island_chains']],
      'spawners':{'type':'zerog_tweaks:tidewraith','weight':10,'minCount':1,'maxCount':1}}
payload=json.dumps(data,indent=2)+'\n'
if a.check:
    assert a.output.read_text()==payload,'Ocean spawn generator/runtime differ'
else:
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(payload)
