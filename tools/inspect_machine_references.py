"""Read-only inventories of installed machine references. Never extracts game assets."""
import argparse
import hashlib
import json
import zipfile
import io
from pathlib import Path

NAMES = ["Mekanism-1.21.1-10.7.19.85.jar", "MekanismGenerators-1.21.1-10.7.19.85.jar",
         "MekanismTools-1.21.1-10.7.19.85.jar", "mekanismcovers-1.3-BETA+1.21.jar",
         "mekanisticrouters-1.2.0.jar", "mekmm-1.21.1-1.4.1.jar"]

def inspect(directory):
    result = []
    for name in NAMES:
        path = directory / name
        if not path.is_file():
            result.append({"file": name, "missing": True})
            continue
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            metadata = next((n for n in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml") if n in names), None)
            interesting = lambda n: any(x in n.lower() for x in ("tank", "upgrade", "port", "transmitter", "gui", "barrel", "chest"))
            result.append({"file": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "entries": len(names), "metadata": archive.read(metadata).decode("utf-8") if metadata else None,
                "license_files": [n for n in names if "license" in n.lower()],
                "reference_classes": [n for n in names if n.endswith(".class") and interesting(n)][:100],
                "reference_art": [n for n in names if n.endswith((".png", ".json")) and interesting(n)][:100]})
    return {"policy": "Read-only reference inventory; no source code, models or texture bytes copied into ZeroG.", "jars": result}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--preview", type=Path, help="Private local contact sheet only; never publish third-party art")
    args = parser.parse_args()
    result = inspect(args.directory)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.preview:
        from PIL import Image, ImageDraw
        samples = []
        for name in NAMES:
            with zipfile.ZipFile(args.directory / name) as archive:
                paths = [n for n in archive.namelist() if n.endswith(".png") and any(k in n for k in (
                    "/gui/base", "/gui/inner_screen", "/block/fluid_tank", "/block/machine", "/item/upgrade", "/textures/block/chemical_tank"))][:8]
                for entry in paths:
                    im = Image.open(io.BytesIO(archive.read(entry))).convert("RGBA")
                    samples.append((name.split("-")[0], entry, im))
        sheet = Image.new("RGB", (1000, 230 * ((len(samples)+3)//4)), "#181d28")
        draw = ImageDraw.Draw(sheet)
        for i, (mod, entry, im) in enumerate(samples):
            x, y = (i%4)*250, (i//4)*230
            im.thumbnail((224, 170), Image.Resampling.NEAREST)
            sheet.paste(im, (x+12,y+16), im)
            draw.text((x+12,y+188), mod, fill="white")
            draw.text((x+12,y+207), entry.split("/")[-1][:30], fill="#99b9d2")
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(args.preview)
    print(json.dumps({"references": [{"file": j["file"], "entries": j.get("entries"), "sha256": j.get("sha256")} for j in result["jars"]], "no_assets_vendored": True}, indent=2))
