"""Read bounded disposable saved chunks; never generate terrain or open player saves.

Face-connected components are observed deposits, not individual feature attempts.
Adjacent veins can merge; diagonal ore cells separate. Boundary-touching deposits
are reported separately because the true component may extend beyond the sample.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/dev"))
import worldscan

PLANETS = ("moon", "mars", "cerulon", "skarn", "eidolon", "solvane")
SITES = ((64, 64), (-80, 96))
DIRECTIONS = ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))

def environmental(name):
    return name.endswith('_rail') or name == 'minecraft:rail' or (
        name.startswith('zerog_tweaks:') and (name.endswith(('_log','_leaves'))
        or any(part in name for part in ('vine','kelp','mushroom','dripstone','cave_berry'))))

def deposits(points, sampled_chunks):
    remaining = set(points)
    interior, boundary = [], []
    while remaining:
        seed = remaining.pop()
        pending = [seed]
        count = 0
        truncated = False
        while pending:
            x,y,z = pending.pop()
            count += 1
            for dx,dy,dz in DIRECTIONS:
                neighbour = (x+dx,y+dy,z+dz)
                if ((x+dx)>>4,(z+dz)>>4) not in sampled_chunks:
                    truncated = True
                if neighbour in remaining:
                    remaining.remove(neighbour)
                    pending.append(neighbour)
        (boundary if truncated else interior).append(count)
    return sorted(interior), sorted(boundary)

def audit(run):
    run = run.resolve()
    if run.parent != ROOT or not run.name.startswith("run-native-ecology-"):
        raise ValueError("Only exact disposable native ecology runs may be inspected")
    worlds = [p for p in run.iterdir() if p.is_dir() and (p / "level.dat").is_file()]
    if len(worlds) != 1:
        raise ValueError("Expected exactly one saved disposable world")
    report = {"scope": "18 saved FULL chunks per Sol planet, face-connected deposits; not vein-attempt sizes or global rarity", "planets": []}
    for planet in PLANETS:
        dim = worlds[0] / "dimensions/zerog_tweaks" / planet
        points = defaultdict(set)
        environment = Counter()
        sampled = set()
        for cx,cz in SITES:
            for dx in range(-1,2):
                for dz in range(-1,2):
                    x,z = cx+dx,cz+dz
                    chunk = worldscan.chunk(str(dim),x,z)
                    if not chunk or chunk.get("Status") not in ("full","minecraft:full"):
                        raise ValueError(f"Missing saved FULL sample: {planet} {x},{z}")
                    sampled.add((x,z))
                    for section in chunk.get("sections",[]):
                        palette = section.get("block_states",{}).get("palette",[])
                        if not any((p["Name"].startswith("zerog_tweaks:") and p["Name"].endswith("_ore")) or environmental(p["Name"]) for p in palette):
                            continue
                        for index,name,y in worldscan.section_blocks(section):
                            if environmental(name): environment[name] += 1
                            if name.startswith("zerog_tweaks:") and name.endswith("_ore"):
                                points[name].add((x*16+(index&15),y,z*16+((index>>4)&15)))
        row = {"dimension": "zerog_tweaks:"+planet, "saved_full_chunks": len(sampled), "ores": {},
               "observed_environmental_blocks": dict(sorted(environment.items())),
               "observed_rail_blocks": sum(v for k,v in environment.items() if k.endswith('_rail') or k=='minecraft:rail')}
        for ore, cells in sorted(points.items()):
            interior,boundary = deposits(cells,sampled)
            if sum(interior)+sum(boundary) != len(cells):
                raise AssertionError("Deposit accounting mismatch")
            row["ores"][ore] = {"observed_blocks": len(cells),
                "interior_component_sizes": interior, "boundary_component_sizes_lower_bounds": boundary,
                "mean_interior_size": sum(interior)/len(interior) if interior else None,
                "max_interior_size": max(interior) if interior else None}
        report["planets"].append(row)
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",type=Path,required=True)
    parser.add_argument("--report",type=Path,required=True)
    args = parser.parse_args()
    result = audit(args.run)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"planets": len(result["planets"]),"chunks": sum(p["saved_full_chunks"] for p in result["planets"]),
                      "ore_blocks": sum(o["observed_blocks"] for p in result["planets"] for o in p["ores"].values())},indent=2))
