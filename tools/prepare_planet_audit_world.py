"""Make a fresh disposable world using only selected hub metadata, no terrain/player copy."""
import argparse
from pathlib import Path
import sys
import shutil

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--hub",type=Path,required=True)
parser.add_argument("--run",type=Path,required=True)
parser.add_argument("--nbt-library",type=Path,required=True)
args=parser.parse_args()
hub=args.hub.resolve(); run=args.run.resolve(); destination=run/"world"
if not run.name.startswith("run-local-planet-") or destination.exists() or hub==destination:
    raise SystemExit("Only a new isolated planet audit directory is permitted.")
sys.path.insert(0,str(args.nbt_library.resolve()))
import nbtlib
level=nbtlib.load(hub/"level.dat")
data=level["Data"]
if int(data["WorldGenSettings"]["seed"])!=0:
    raise SystemExit("Expected the selected seed-zero hub.")
data["WorldGenSettings"]["generate_features"]=nbtlib.Byte(1)
data["LevelName"]=nbtlib.String("ZeroG isolated planet regeneration audit")
data["GameType"]=nbtlib.Int(1)
data["allowCommands"]=nbtlib.Byte(1)
data.pop("Player",None)
destination.mkdir(parents=True)
level.save(destination/"level.dat")
print("Fresh isolated terrain; original hub metadata, terrain and player data untouched: "+str(destination))
