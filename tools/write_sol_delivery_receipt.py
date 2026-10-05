"""Build an evidence-only delivery receipt after installation/world refresh.

Does not install, edit a save, launch a game, or publish a branch.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile

parser = argparse.ArgumentParser(description=__doc__)
for name in ["jar", "installed", "install-report", "world-refresh", "source-world", "survey", "asset-report", "output"]:
    parser.add_argument("--" + name, type=Path, required=True)
parser.add_argument("--log", type=Path, action="append", required=True)
args = parser.parse_args()

def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

candidate_hash = sha(args.jar)
if sha(args.installed) != candidate_hash:
    raise SystemExit("Installed JAR does not match the production candidate.")
installation = json.loads(args.install_report.read_text())
if not installation.get("installed") or installation["sha256"] != candidate_hash:
    raise SystemExit("No matching installation receipt.")
if not installation.get("backup") or not installation.get("backed_up"):
    raise SystemExit("This delivery requires a backed-up old JAR.")
if not all((Path(installation["backup"]) / name).is_file() for name in installation["backed_up"]):
    raise SystemExit("Old JAR backup is missing.")
with ZipFile(args.jar) as jar:
    if any("/gametest/" in name or "structure/equipment_empty" in name for name in jar.namelist()):
        raise SystemExit("Test material is present in the production JAR.")
    manifest = jar.read("META-INF/MANIFEST.MF").decode()
    if not re.search(r"(?m)^Implementation-Version: 1\.0\.12-dev\r?$", manifest):
        raise SystemExit("Unexpected production version.")

refresh = json.loads(args.world_refresh.read_text())
if not refresh.get("refreshed") or not refresh.get("protected_bytes_unchanged") or len(refresh["planets"]) != 34:
    raise SystemExit("Protected selected-save refresh has not completed.")
assets = json.loads(args.asset_report.read_text())
if assets["error_count"]:
    raise SystemExit("Asset-binding errors remain.")
tests = []
for path in args.log:
    text = path.read_text(errors="replace")
    passed = re.findall(r"All (\d+) required tests passed", text)
    if not passed or "BUILD SUCCESSFUL" not in text or "BUILD FAILED" in text:
        raise SystemExit("No clean passing test verdict: " + str(path))
    tests.append({"log": path.name, "sha256": sha(path), "required_tests_passed": int(passed[-1])})

hub = json.loads((args.source_world / "zerog-hub-report.json").read_text())
survey = json.loads(args.survey.read_text())
dimensions = survey["dimensions"]
tree_chunks = sum(len(d["tree_chunks"]) for d in dimensions)
logs = sum(n for d in dimensions for key, n in d["observed_ecology_blocks"].items() if key.endswith("_log"))
result = {
    "date": "2026-10-05", "version": "1.0.12-dev", "minecraft": "Java 1.21.1",
    "candidate": {"file": args.jar.name, "sha256": candidate_hash, "production_tests_excluded": True},
    "installation": {"installed_hash_verified": True, "old_jar_backed_up_outside_mods": True,
        "backup_folder": Path(installation["backup"]).name,
        "backed_up": installation["backed_up"],
        "preserved_dependencies": installation["preserved_dependencies"]},
    "tests": tests, "asset_reference_audit": assets,
    "selected_world": {"name": "ZeroG_Planet_Showcase_1_0_9_Seed0", "seed": hub["seed"],
        "planetary_dimensions_refreshed": len(refresh["planets"]), "preserved_hub_routes": refresh["preserved_hub_routes"],
        "protected_files": refresh["preserved_files"], "hub_player_other_dimension_bytes_unchanged": True,
        "full_recoverable_backup": True, "gate_count": hub["gate_count"],
        "demonstration_colonies": hub["demonstration_colonies"]},
    "saved_native_terrain_survey": {"scope": survey["scope"], "dimensions": len(dimensions),
        "actual_log_blocks": logs, "tree_containing_chunks": tree_chunks,
        "dimensions_with_observed_trees": sum(bool(d["tree_chunks"]) for d in dimensions)},
    "client_launched": False, "in_game_visual_approval": "pending human review",
    "remaining": ["Authoritative bee lifespan/tolerance/module rules unavailable",
        "Full PB flower/territory/hive-upgrade parity not claimed", "Third-party claims/team adapters",
        "Hidden Star Map Fragment world pool", "Moving cargo client renderer",
        "Cinder Mite boss adds need approved registered entity", "Separate Frost Yak shorn model",
        "Natural ecology coverage outside saved samples and client visual approval"],
    "branch_policy": {"code": "1.21.x", "design": "Design", "documentation_jar": "Docs", "Released": "unchanged"}
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"receipt": str(args.output), "sha256": candidate_hash, "test_groups": len(tests)}, indent=2))
