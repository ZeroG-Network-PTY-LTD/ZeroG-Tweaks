"""Mechanical repair: each stair references its own registered full-block base.

Base blocks register before stairs, avoiding forward DeferredHolder resolution.
This does not change IDs, textures or models. Run against the code worktree.
"""
import argparse
import re
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("code",type=Path)
args=parser.parse_args()
path=args.code/"src/main/java/net/zerog/tweaks/registry/BlockInit.java"
text=path.read_text()
fields=set(re.findall(r"public static final DeferredBlock<[^>]+> (\w+) =",text))
stairs=[]
lines=[]
for line in text.splitlines():
    match=re.search(r"DeferredBlock<Block> (\w+)_STAIRS = BLOCKS.register\(\"([^\"]+)\"",line)
    if match and "StairBlock" in line:
        base=match[1]
        if base.endswith("_BRICK"):
            base+="S"
        elif base in {"CHARWOOD","HOARWOOD","SHARDWOOD","GILDWOOD"}:
            base+="_PLANKS"
        if base not in fields:
            raise SystemExit("Missing stair base "+base)
        stairs.append(f'    public static final DeferredBlock<Block> {match[1]}_STAIRS = BLOCKS.register("{match[2]}", () -> new net.minecraft.world.level.block.StairBlock({base}.get().defaultBlockState(), BlockBehaviour.Properties.ofFullCopy({base}.get())));')
    else:
        lines.append(line)
text="\n".join(lines)+"\n"
marker="    // ---- flower pots (vanilla potted_* counterparts) ----"
assert text.count(marker)==1 and len(stairs)>20
text=text.replace(marker,"    // Stairs register after their full-block bases; IDs are unchanged.\n"+"\n".join(stairs)+"\n\n"+marker)
path.write_text(text)
print(f"Repaired {len(stairs)} base-state and material property contracts")
