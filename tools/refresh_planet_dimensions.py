"""Replace only the named showcase's ZeroG planets from a verified isolated hub.

Dry-run by default. A complete recoverable backup precedes writes. No terrain is
deleted: old planetary folders are moved into the backup before replacement.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sys

PLANETS = ["moon", "mars", "cerulon", "skarn", "eidolon", "solvane"] + [
    f"g{galaxy}_{planet}" for galaxy in range(2, 6) for planet in
    ["p1", "p2", "p3", "p4", "p5", "p6", "moons"]]
SAVE_NAME = "ZeroG_Planet_Showcase_1_0_9_Seed0"
LEDGER = "data/zerog_planet_gates.dat"

def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def protected_files(world):
    result = {}
    for path in world.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(world).as_posix()
        if relative == LEDGER or relative.startswith("zerog-refresh-"):
            continue
        if any(relative.startswith(f"dimensions/zerog_tweaks/{name}/") for name in PLANETS):
            continue
        result[relative] = digest(path)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--nbt-library", required=True, type=Path)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    source, target = args.source.resolve(), args.destination.resolve()
    if target.name != SAVE_NAME or target.parent.name != "saves":
        raise SystemExit("Only the human-selected 1.0.9 showcase is allowed.")
    if not target.is_dir() or not source.is_dir() or source == target or source.is_relative_to(target) or target.is_relative_to(source):
        raise SystemExit("Existing, distinct source and selected save required.")
    sys.path.insert(0, str(args.nbt_library.resolve()))
    import nbtlib
    report = json.loads((source / "zerog-hub-report.json").read_text())
    if report["seed"] != 0 or report["gate_count"] != 68 or len(report["planets"]) != 34:
        raise SystemExit("Isolated source has not passed all 34 planet/gate checks.")
    if report.get("demonstration_colonies", True):
        raise SystemExit("Source must have the obsolete demonstration colonies disabled.")
    old_level = nbtlib.load(target / "level.dat")
    new_level = nbtlib.load(source / "level.dat")
    if int(old_level["Data"]["WorldGenSettings"]["seed"]) != int(new_level["Data"]["WorldGenSettings"]["seed"]):
        raise SystemExit("World seed mismatch.")
    for planet in PLANETS:
        if not (source / "dimensions" / "zerog_tweaks" / planet / "region").is_dir():
            raise SystemExit(f"No pregenerated region for {planet}.")
    old = nbtlib.load(target / LEDGER)
    new = nbtlib.load(source / LEDGER)
    old_data, new_data = old["data"], new["data"]
    refreshed_ids = {f"zerog_tweaks:{name}" for name in PLANETS}
    preserved = [g for g in old_data["gates"] if str(g["dimension"]) not in refreshed_ids]
    incoming = [g for g in new_data["gates"] if str(g["dimension"]) in refreshed_ids]
    if len(incoming) != 34 or {str(g["dimension"]) for g in incoming} != refreshed_ids or any(str(g["target"]) != "minecraft:overworld" for g in incoming) or len([g for g in preserved if str(g["dimension"]) == "minecraft:overworld"]) != 34:
        raise SystemExit("Expected 34 existing hub routes and 34 validated return routes.")
    result = {"source": str(source), "destination": str(target), "planets": PLANETS,
              "refreshed": False, "preserved_hub_routes": len(preserved), "backup": None}
    if not args.refresh:
        print(json.dumps(result, indent=2)); return
    # Locks alone can be stale. The caller must independently verify Minecraft is closed.
    before = protected_files(target)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S-UTC")
    backup = target.parent.parent / "zerog-world-backups" / (SAVE_NAME + "-" + stamp)
    shutil.copytree(target, backup / "complete-save")
    if protected_files(backup / "complete-save") != before or protected_files(target) != before:
        raise RuntimeError("Save changed during backup; close all game/server processes.")
    staged=backup/"validated-incoming-planets"
    for planet in PLANETS:
        shutil.copytree(source / "dimensions" / "zerog_tweaks" / planet,staged/planet)
    moved=[]
    installed=[]
    try:
        for planet in PLANETS:
            destination = target / "dimensions" / "zerog_tweaks" / planet
            if destination.exists():
                parked = backup / "replaced-planets" / planet
                parked.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(parked))
                moved.append(planet)
            shutil.move(str(staged/planet),str(destination))
            installed.append(planet)
        old_data["gates"] = nbtlib.List[nbtlib.Compound](preserved + incoming)
        for key in ["prepared", "inspectionEnabled", "inspectionPrepared"]:
            old_data[key] = new_data[key]
        retained_inspections=[v for v in old_data.get("inspectionVillages", []) if str(v["dimension"]) not in refreshed_ids]
        incoming_inspections=[v for v in new_data.get("inspectionVillages", []) if str(v["dimension"]) in refreshed_ids]
        old_data["inspectionVillages"]=nbtlib.List[nbtlib.Compound](retained_inspections+incoming_inspections)
        old.save(target / LEDGER)
        if protected_files(target) != before:
            raise RuntimeError("Protected hub/player/other-dimension bytes changed.")
        result.update(refreshed=True, backup=str(backup), preserved_files=len(before), protected_bytes_unchanged=True)
        (target / "zerog-refresh-report.json").write_text(json.dumps(result, indent=2) + "\n")
    except Exception:
        for planet in reversed(installed):
            destination=target/"dimensions"/"zerog_tweaks"/planet
            if destination.exists():
                parked=backup/"failed-incoming-planets"/planet
                parked.parent.mkdir(parents=True,exist_ok=True)
                shutil.move(str(destination),str(parked))
        for planet in reversed(moved):
            shutil.move(str(backup/"replaced-planets"/planet),str(target/"dimensions"/"zerog_tweaks"/planet))
        shutil.copy2(backup/"complete-save"/LEDGER,target/LEDGER)
        print("Refresh rolled back; original save also preserved at " + str(backup / "complete-save"), file=sys.stderr)
        raise
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
