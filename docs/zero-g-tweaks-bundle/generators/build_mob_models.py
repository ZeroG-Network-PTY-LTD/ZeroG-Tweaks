"""Build editable Blockbench and GeckoLib assets from the canonical mob sheets.

The design boxes and palettes live in mobs_data.py and mobs_food.py.  This
script never modifies either source.  Run from any directory with Python 3 and
Pillow installed.  Assets are pixel drawn at 8 texture pixels per model unit;
they are original texture work, not a resized version of the reference sheets.
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import math
import re
import uuid
from pathlib import Path

from PIL import Image, ImageDraw

from mobs_data import MOBS
from mobs_food import M2
from mob_anatomy import refine_boxes
from mob_faces import refine_face

ROOT = Path(__file__).resolve().parents[3]
PROJECTS = ROOT / "docs/zero-g-tweaks-bundle/blockbench/mobs"
ASSETS = ROOT / "src/main/resources/assets/zerog_tweaks"
SCALE = 8
PAD = 2
FACE_ORDER = ("north", "south", "east", "west", "up", "down")
NAMESPACE = uuid.UUID("4198ddf0-558c-45bc-a68c-c0194218bb21")


def uid(*parts: object) -> str:
    return str(uuid.uuid5(NAMESPACE, "/".join(map(str, parts))))


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rgb(hex_color: str) -> tuple[int, int, int]:
    return tuple(bytes.fromhex(hex_color.removeprefix("#")))


def clamp(v: float) -> int:
    return min(255, max(0, int(v)))


def part_group(label: str, box: tuple[float, ...], index: int) -> str:
    name = label.lower()
    x0, y0, z0, x1, y1, z1 = box
    side = "left" if (x0 + x1) < -0.05 else "right"
    if re.search(r"\bears?\b",name):
        return f"{side}_ear"
    if "antler" in name:
        return "antlers"
    if "wool" in name or "hump" in name:
        return "wool"
    if "orbiting" in name:
        return "orbit"
    if "corona rays" in name:
        return "corona"
    if "neck" in name:
        return "neck"
    if name.startswith("segment "):
        return "segment_"+name.split()[-1]
    if "jaw" in name:
        return "jaw"
    if "mouth" in name:
        return "mouth"
    if any(k in name for k in ("leg", "hoof", "hooves", "feet", "foot", "paw", "toe")):
        return f"leg_{side}_{round((z0+z1)/2, 2)}".replace("-", "m").replace(".", "p")
    if re.search(r"\b(?:wings?|fins?)\b",name) and "tail" not in name and "seam" not in name:
        if abs(x0+x1)<.01:
            return "dorsal_fin"
        return f"{side}_wing"
    if any(k in name for k in ("tail", "stinger", "flame tip")):
        return "tail"
    if any(k in name for k in ("head", "helm", "hat", "eye", "horn", "snout", "muzzle", "nostril", "nose", "mand", "maw", "teeth", "fang", "incisor", "antenna", "beak", "visor", "face", "brow", "pupil")):
        return "head"
    if re.search(r"\b(?:arms?|claws?|pincers?|fists?)\b",name):
        return f"{side}_arm"
    return "body"


def pattern_color(base: tuple[int, int, int], pattern: str, x: int, y: int,
                  face: str, seed: int, emissive: bool, height: int) -> tuple[int, int, int, int]:
    n = int.from_bytes(hashlib.blake2s(f"{seed}:{x//2}:{y//2}".encode(), digest_size=2).digest(), "big")
    noise = (n % 17) - 8
    light = 1.14 if face == "up" else 0.76 if face == "down" else 0.88 if face in ("east", "west") else 1.0
    # Three restrained value bands keep the surface readable at game distance.
    gradient = (1 - y / max(1, height - 1)) * 12 - 6
    delta = noise * 0.45 + gradient
    if pattern == "fur":
        delta += 9 if (x//3 + y//7 + seed) % 7 == 0 else -2
    elif pattern == "stripes":
        delta += -14 if (y // SCALE) % 4 == 0 else 2
    elif pattern == "spots":
        delta += 15 if ((x // 8) * 7 + (y // 8) * 11 + seed) % 9 == 0 else 0
    elif pattern == "cracks":
        delta += 27 if (x//2 * 5 + y//2 * 3 + seed) % 29 < 2 else -3
    elif pattern == "crystal":
        delta += 18 if (x - y) % 16 < 3 else -7 if (x + y) % 16 < 3 else 3
    elif pattern == "rivets":
        delta += 32 if x % 14 in (2, 3) and y % 14 in (2, 3) else -7 if x % 14 in (4, 5) else 0
    elif pattern in ("scales", "chitin", "horn"):
        delta += -12 if (y + ((x//8)%2)*3) % 9 == 0 else 5 if y%9==1 else 0
    elif pattern in ("moss", "leaf", "kelp"):
        delta += 11 if (x//3 + y//4 + seed)%5==0 else -5 if (x//5+y//7)%3==0 else 0
    elif pattern in ("plate", "brass", "copper", "rusted"):
        delta += 7 if (y+seed)%13==0 else -4
    elif pattern == "glow" or emissive:
        delta += 16 if (x + y) % 6 < 2 else 0
    alpha=255
    if pattern=="membrane" and y>height-8 and ((x//5+seed)%11 in (0,1)):
        alpha=0
    return (*[clamp(c * light + delta) for c in base], alpha)


def remastered_pixel(base, pattern, x, y, face, seed, emissive, height, width, label, planar=False):
    """Original clustered pixel art; broad color ramps remain readable at distance."""
    name=label.lower()
    tx,ty=x/max(1,width-1),y/max(1,height-1)
    # Five discrete tone bands rather than a blurry continuous gradient.
    band=round((1-ty)*4)/4
    light={"up":1.08,"down":0.85,"east":0.96,"west":0.96}.get(face,1.0)
    grain=((x//3*17+y//3*29+seed*13)%11-5)*0.55
    delta=(band-.5)*23+grain
    material=pattern.lower()
    if material.startswith('ender_eye_'):
        # Original pixel art based on the supplied six-panel eye reference.
        # Preserve a transparent pointed outline and the dark pupil: do not
        # flatten it into a rectangular glow stripe or replace the mob body.
        nx=(int(tx*32)+.5)/16-1;ny=(int(ty*32)+.5)/16-1
        if abs(nx)+.52*abs(ny)>1.0 or abs(ny)>.93:return (0,0,0,0)
        r=math.hypot(nx,ny);angle=math.atan2(ny,nx)
        theme=material.removeprefix('ender_eye_')
        pupil=r<.29 if theme in ('dying_star','crater_drifter') else abs(nx)<.115 and abs(ny)<.62
        if pupil:return (10,9,17,255)
        if theme=='prismling':
            ramp=[(102,234,242),(196,128,255),(248,136,219),(255,219,108)]
            col=ramp[int((angle+math.pi)/(2*math.pi)*len(ramp))%len(ramp)]
            level=.5 if r>.82 else .78 if r>.62 else 1.0
            if abs((nx+ny)*7-round((nx+ny)*7))<.08:level+=.15
        elif theme=='flare_sprite':
            wave=(angle*3-r*14)%(2*math.pi)
            col=(255,205 if wave<2 else 136,62 if wave<2 else 27);level=.6 if r>.83 else 1
        elif theme=='dying_star':
            col=(121,97,236) if (angle*3+r*14)%(2*math.pi)<2.2 else (48,39,113)
            level=1.1 if .29<r<.38 else .8 if r>.82 else 1
        elif theme=='crater_drifter':
            col=(164,171,179);level=.62 if r>.83 else .9+(int(tx*12)*7+int(ty*12)*13)%5*.035
            if (int(tx*14)*7+int(ty*14)*11)%19<3:level*=.48
        elif theme=='ash_strider':
            col=(255,123,35) if (int(tx*18)*5+int(ty*18)*3)%13<3 or .29<r<.42 else (48,43,46)
            level=.55 if r>.82 else 1
        else:
            col=(75,223,218) if (int(tx*16)+int(ty*16)*3)%7<4 else (179,158,108)
            level=.5 if r>.84 else 1
        if nx<-.18 and ny<-.25 and r<.72 and abs(nx+ny+.68)<.12:col=(236,242,251);level=1
        return (*[clamp(c*level) for c in col],255)
    if name=='eyes':
        # Reference: one deliberate three-cell horizontal eye, not tiny shiny beads.
        # Keep both side faces identical and avoid arbitrary subpixel catchlights.
        centre = width//3 <= x < width-width//3
        if emissive:
            return (*[clamp(c*.65 if centre else c*.65+89) for c in base],255)
        if centre:
            return (19,22,29,255)
        return (*[clamp(c*.15+210) for c in base],255)
    if "nostril" in name or "nose" in name or "mouth" in name:
        delta-=7 if .2<tx<.8 and .25<ty<.85 else 0
    if "feather" in name or "wing" in name and material=="fur":
        delta+=8 if x%12<3 else -6 if x%12>9 else 0
        delta-=5 if (y+x//12*3)%18==17 else 0
    elif material=="fur" or any(s in name for s in ("wool","fluff","mane","bristle")):
        # Layered short fur clusters; lower tufts become darker.
        delta+=7 if (x//4+(y//9)*3+seed)%7==0 and y%9<5 else -3
        delta-=5 if y%11==10 else 0
    elif material in ("scales","chitin") or any(s in name for s in ("scale","carapace","shell")):
        row=y//8; sx=(x+(row%2)*5)%10
        delta+=-12 if y%8==7 or sx==9 else 7 if y%8==1 and sx<7 else 0
    elif material=="crystal":
        delta+=19 if (x-y//2)%24<4 else -10 if (x+y//2)%24>20 else 0
    elif "horn" in name or "tusk" in name or material=="horn":
        delta+=-8 if y%10 in (8,9) else 5 if y%10==0 else 0
    elif material in ("plate","brass","copper","rusted","rivets"):
        delta+=9 if x%32<2 or y%32<2 else -8 if x%32==31 or y%32==31 else 0
        if material=="rusted":delta-=12 if (x//5*7+y//6*3+seed)%13<3 else 0
    elif material in ("moss","leaf","kelp"):
        delta+=10 if (x//5+y//7*3+seed)%7<2 else -5
    elif material=="stripes":
        delta-=12 if y%24<5 else 0
    elif material=="spots":
        delta+=12 if (x//12*7+y//12*11+seed)%9==0 else 0
    elif material=="cracks":
        delta+=20 if (x//3*5+y//3*3+seed)%29<2 else -2
    if emissive:
        light=1.0
        delta=(band-.5)*12+(8 if (x-y//2)%19<3 else 0)
    # Narrow painted edge accents make joints/plates readable without black outlines.
    if width>=16 and height>=16:
        delta+=4 if x==0 or y==0 else -4 if x==width-1 or y==height-1 else 0
    alpha=191 if "translucent gel" in name else 255
    if planar and width>=8 and height>=8:
        if "membrane" in name:
            # Veins fan from the attachment edge. Only authored torn tips get holes.
            delta-=9 if abs((tx*3)%1-ty)<.035 else 0
            if "torn" in name and ty>.73 and .35<tx<.55:
                alpha=0
        elif "fin" in name or "wing" in name:
            delta+=7 if x%12<2 else -4 if x%12==11 else 0
            # A stepped trailing edge, retaining the centre and attachment edge.
            if ty>.92 and (x//8)%3==0:
                alpha=0
        elif "cloak" in name or "tattered" in name:
            if ty>.9 and (x//8)%4==0:alpha=0
    cool=(1-band)*3
    return (clamp(base[0]*light+delta-cool),clamp(base[1]*light+delta),clamp(base[2]*light+delta+cool),alpha)


def faces_for_box(box: tuple[float, ...], cursor: tuple[int, int]) -> tuple[dict, dict, int]:
    x0, y0, z0, x1, y1, z1 = box
    w = max(1, round((x1 - x0) * SCALE))
    h = max(1, round((y1 - y0) * SCALE))
    d = max(1, round((z1 - z0) * SCALE))
    widths = {"north": w, "south": w, "east": d, "west": d, "up": w, "down": w}
    heights = {"north": h, "south": h, "east": h, "west": h, "up": d, "down": d}
    u, v = cursor
    faces = {}
    for face in FACE_ORDER:
        fw, fh = widths[face], heights[face]
        faces[face] = {"uv": [u, v, u + fw, v + fh], "rotation": 0, "texture": 0}
        u += fw + PAD
    return faces, {"width": u - cursor[0], "height": max(heights.values())}, u


def group_pivot(name: str, boxes: list[tuple]) -> list[float]:
    if name.startswith("leg_") or name.endswith("arm"):
        y = max(b[5] for b in boxes)
    elif name.endswith("wing"):
        y = sum((b[2] + b[5]) / 2 for b in boxes) / len(boxes)
    else:
        y = sum((b[2] + b[5]) / 2 for b in boxes) / len(boxes)
    x = sum((b[1] + b[4]) / 2 for b in boxes) / len(boxes)
    z = sum((b[3] + b[6]) / 2 for b in boxes) / len(boxes)
    if name == "head":
        z = max(b[6] for b in boxes)
    if name in ("jaw","mouth"):
        y,z=max(b[5] for b in boxes),max(b[6] for b in boxes)
    if name=="neck":
        y,z=min(b[2] for b in boxes),max(b[6] for b in boxes)
    if name=="tail":
        z=min(b[3] for b in boxes)
    if name.endswith("ear"):
        y = min(b[2] for b in boxes)
    if name.endswith("wing"):
        x = max(b[4] for b in boxes) if x < 0 else min(b[1] for b in boxes)
    if name in ("orbit", "corona", "root"):
        x, y, z = 0, 0, 0
    return [round(x, 3), round(y, 3), round(z, 3)]


def keyframe(t: float, channel: str, value: list[float], label: str) -> dict:
    return {"channel": channel, "data_points": [dict(zip(("x", "y", "z"), value))],
            "uuid": uid(label, channel, t), "time": t, "color": -1, "interpolation": "linear"}


def animations_for(key: str, groups: dict[str, dict]) -> tuple[list[dict], dict]:
    bb_animations = []
    gecko = {}
    specials = {"moon_hopper": "hop", "azure_fowl": "glide", "glimmerfish": "swim",
                "deep_eel": "swim", "ice_leech": "slither", "dune_burrower": "burrow",
                "regolith_crawler": "burrow", "sand_skitter": "burrow", "slag_boar": "charge",
                "cinder_hound": "run", "rime_stalker": "run", "crystal_stag": "graze",
                "frost_yak": "graze", "dust_grazer": "graze", "sun_colossus": "slam",
                "prism_sentinel": "orbit", "dying_star": "corona", "crater_drifter": "float",
                "flare_sprite": "fly", "scorch_wyrmling": "glide", "eidolon_captain": "float"}
    actions = [("idle", 2.0), ("walk", 0.8), ("attack", 0.5)]
    if key in specials:
        actions.append((specials[key], 4.0 if key in ("prism_sentinel", "dying_star") else 1.2))
    if key in ("crystal_stag", "frost_yak"):
        actions.append(("sheared", 1.0))
    for action, duration in actions:
        animators = {}
        bones = {}
        for name, group in groups.items():
            motion = 0
            channel = "rotation"
            axis = 0
            if action == "idle":
                if name == "head" and group.get("children"): motion, axis = 3, 0
                elif name == "tail": motion, axis = 7, 1
                elif name.endswith("wing"): motion, axis = 7, 2
                elif name.endswith("ear"): motion, axis = 5, 2
                elif name.startswith('stalk_'):motion,axis=6 if name.endswith('_l') else -6,1
                elif name == "body": motion, axis, channel = 0.4, 1, "position"
            elif action in ("walk","run","charge"):
                if name.startswith("leg_"):
                    stem = name.removesuffix("_shin").removesuffix("_foot")
                    side = "left" if "left" in name else "right"
                    same_side = sorted([g for g in groups if g.startswith("leg_") and side in g and not g.endswith(("_shin", "_foot"))], key=lambda g: groups[g]["pivot"][2])
                    parity = (-1) ** (same_side.index(stem) + (side == "right"))
                    amplitude = -10 if name.endswith("_shin") else 4 if name.endswith("_foot") else 22
                    motion, axis = amplitude * parity, 0
                    if action != "walk": motion*=1.4
                elif name == "tail": motion, axis = 9, 1
                elif name.endswith("wing"): motion, axis = 12 if "left" in name else -12, 2
                elif name == "body": motion, axis, channel = 0.5, 1, "position"
            elif action == "attack":
                if name == "head" and group.get("children"): motion, axis = -18, 0
                elif name == "jaw":motion,axis=18,0
                elif name == "mouth":motion,axis,channel=-.25,1,"position"
                elif name.endswith("arm"): motion, axis = -32, 0
                elif name == "body": motion, axis = 5, 0
            elif action in ("hop", "float", "fly") and name == "root":
                motion, axis, channel = (5 if action == "hop" else 1.5), 1, "position"
            elif action=="hop" and name.startswith("leg_"):
                # Rabbit reference: paired hind legs push together, forelegs tuck.
                front=group["pivot"][2]<0
                motion,axis=(-28 if front else 38),0
                if name.endswith("_shin"):motion*=-.5
                elif name.endswith("_foot"):motion*=.5
            elif action in ("glide", "fly") and name.endswith("wing"):
                motion, axis = 28 if "left" in name else -28, 2
            elif action in ("swim", "slither") and name in ("body", "tail", "head"):
                motion, axis = (14 if name == "tail" else 4), 1
            elif action == "graze" and name == "head":
                motion, axis = 22, 0
            elif action == "burrow" and name == "root":
                motion, axis, channel = -5, 1, "position"
            elif action in ("charge", "run") and name == "body":
                motion, axis = 5, 0
            elif action == "slam" and name.endswith("arm"):
                motion, axis = -75, 0
            elif action in ("orbit", "corona") and name == action:
                motion, axis = 360, 1 if action == "orbit" else 2
            elif action == "sheared" and name in ("antlers", "wool"):
                motion, axis, channel = 0.01 if name == "antlers" else 0.84, 0, "scale"
            if key=="dune_burrower" and name.startswith("segment_") and action in ("idle","walk","burrow"):
                motion,axis=4 if action=="idle" else 8,1
            if not motion:
                continue
            values = []
            if action in ("orbit", "corona"):
                values = [(0, 0), (duration, motion)]
            elif action == "sheared":
                values = [(0, motion), (duration, motion)]
            elif action in ("attack", "hop", "burrow", "graze", "slam"):
                values = [(0, 0), (duration / 2, motion), (duration, 0)]
            else:
                values = [(0, 0), (duration / 4, motion), (3 * duration / 4, -motion), (duration, 0)]
            if key=="dune_burrower" and name.startswith("segment_") and action in ("idle","walk","burrow"):
                phase=int(name.split("_")[-1])*.45
                values=[(duration*i/16,math.sin(i/16*math.tau+phase)*motion) for i in range(17)]
            bbf = []
            gf = {}
            for t, amount in values:
                xyz = [0, 0, 0]
                xyz[axis] = amount
                if channel == "scale":
                    xyz = [amount, amount, amount]
                bbf.append(keyframe(round(t, 3), channel, xyz, f"{key}:{action}:{name}"))
                gf[str(round(t, 3))] = xyz
            animators[group["uuid"]] = {"name": name, "type": "bone", "keyframes": bbf}
            bones[name] = {channel: gf}
        bb_animations.append({"uuid": uid(key, action), "name": f"animation.zerog_tweaks.{key}.{action}",
                              "loop": "once" if action == "attack" else "loop", "override": False,
                              "length": duration, "snapping": 20, "animators": animators})
        gecko[f"animation.zerog_tweaks.{key}.{action}"] = {
            "loop": action != "attack", "animation_length": duration, "bones": bones}
    return bb_animations, {"format_version": "1.8.0", "animations": gecko}


def build(key: str, spec: dict) -> dict:
    spec=dict(spec)
    spec["parents"]=dict(spec.get("parents",{}))
    namespace = spec.get("namespace", "zerog_tweaks")
    assets = ROOT / "src/main/resources/assets" / namespace
    projects = ROOT / "docs/shattered-skies/blockbench" if namespace == "shatteredskies" else PROJECTS
    palette = spec["pal"]
    entries = []
    prior = "body"
    raw_boxes = spec["boxes"] if spec.get("authored_bones") else refine_boxes(key, spec)
    for i, raw in enumerate(raw_boxes):
        label, x0, y0, z0, x1, y1, z1, color_key, pattern = raw
        if label:
            prior = label
        label = label or prior
        box = (x0, y0, z0, x1, y1, z1)
        name=label.lower()
        planar=any(word in name for word in ("membrane", "fin", "fire wings", "cloak")) and not any(word in name for word in ("finger", "fist", "fins ridge"))
        plane_axis=None
        if planar:
            plane_axis=min(range(3),key=lambda a:box[a+3]-box[a])
            coords=list(box)
            coords[plane_axis]=coords[plane_axis+3]=(box[plane_axis]+box[plane_axis+3])/2
            box=tuple(coords)
        entries.append({"label": label, "box": box, "color_key": color_key,
                        "plane_axis":plane_axis,"pattern": pattern, "group": spec["authored_bones"][i] if spec.get("authored_bones") else part_group(label, box, i)})

    entries=refine_face(key,spec,entries)
    if key=="dying_star":
        for entry in entries:
            if (entry['label']=="Archon Vael" and entry['box'][1]>=40) or entry['label']=="Crown":
                entry['group']='head'

    # Eyes follow their original head/helm attachment while gaining separate controls.
    for i,entry in enumerate(entries):
        label=entry["label"].lower()
        if label=="eyes":
            parent=entry["group"]
            name=f"eye_{i:02d}"
            spec["parents"][name]=parent
            entry["group"]=name
            if entry["color_key"]=="eye" and "stalk" in label:
                entry["label"]="Eyes"

    if not spec.get("authored_bones"):
        names={e["group"] for e in entries}
        if "head" not in names and any(n.startswith("eye_") for n in names):
            spec["parents"].setdefault("head","body")
        for entry in entries:
            label=entry["label"].lower()
            if key in ("frost_warden","eidolon_captain") and any(word in label for word in ("glaive","cutlass","lantern")):
                entry["group"]="left_arm" if entry["box"][0]+entry["box"][3]<0 else "right_arm"
                if key=="eidolon_captain" and "cutlass" in label:
                    b=list(entry["box"]);b[0]+=2;b[3]+=2;entry["box"]=tuple(b)

    leg_anchors = [] if spec.get("authored_bones") else [e for e in entries if e["label"].lower().startswith("upper ") and e["group"].startswith("leg_")]
    for entry in entries:
        if not entry["group"].startswith("leg_"):
            continue
        label = entry["label"].lower()
        if label.startswith("upper "):
            continue
        side = "left" if sum((entry["box"][0], entry["box"][3])) < 0 else "right"
        candidates = [e for e in leg_anchors if side in e["group"]]
        if candidates:
            nearest = min(candidates, key=lambda e: abs((e["box"][2]+e["box"][5])-(entry["box"][2]+entry["box"][5])))
            stem = nearest["group"]
            entry["group"] = stem + ("_shin" if label.startswith("lower ") else "_foot")

    # Shelf pack each cube's six face tiles without overlap or clipping.
    placements = []
    atlas = 512
    while True:
        placements.clear()
        x = y = row_h = 2
        for entry in entries:
            _, dims, _ = faces_for_box(entry["box"], (0, 0))
            if dims["width"] + 4 > atlas:
                break
            if x + dims["width"] + 2 > atlas:
                x, y, row_h = 2, y + row_h + PAD, 2
            placements.append((x, y))
            x += dims["width"] + PAD
            row_h = max(row_h, dims["height"])
        if len(placements) == len(entries) and y + row_h + 2 <= atlas:
            break
        atlas *= 2
        if atlas > 4096:
            raise ValueError(f"{key}: texture atlas too large")

    base = Image.new("RGBA", (atlas, atlas), (0, 0, 0, 0))
    glow = Image.new("RGBA", (atlas, atlas), (0, 0, 0, 0))
    groups: dict[str, dict] = {}
    elements = []
    for i, (entry, cursor) in enumerate(zip(entries, placements)):
        label, box = entry["label"], entry["box"]
        group_name = entry["group"]
        group = groups.setdefault(group_name, {"uuid": uid(key, "bone", group_name), "children": []})
        faces, _, _ = faces_for_box(box, cursor)
        if entry["plane_axis"] is not None:
            visible=(("east","west"),("up","down"),("north","south"))[entry["plane_axis"]]
            faces={name:data for name,data in faces.items() if name in visible}
        color = rgb(palette.get(entry["color_key"], next(iter(palette.values()))))
        emissive = entry["pattern"] == "glow" or entry["pattern"].startswith('ender_eye_') or any(s in label.lower() for s in ("glowing", "emissive"))
        reflected=(-box[3],box[1],box[2],-box[0],box[4],box[5])
        canonical=min(box,reflected)
        seed=int.from_bytes(hashlib.blake2s(repr((canonical,entry["color_key"],entry["pattern"])).encode(),digest_size=2).digest(),"big")
        for face, face_data in faces.items():
            u0, v0, u1, v1 = face_data["uv"]
            for v in range(v0, v1):
                for u in range(u0, u1):
                    pixel = remastered_pixel(color, entry["pattern"], u-u0, v-v0, face, seed, emissive, v1-v0, u1-u0, label, entry["plane_axis"] is not None)
                    base.putpixel((u, v), pixel)
                    if emissive and (not entry['pattern'].startswith('ender_eye_') or max(pixel[:3])>80):
                        glow.putpixel((u, v), pixel)
        x0, y0, z0, x1, y1, z1 = box
        element_id = uid(key, "cube", i)
        group["children"].append(element_id)
        elements.append({"name": re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_") + f"_{i:02d}",
                         "box_uv": False, "rescale": False, "locked": False,
                         "light_emission": 15 if emissive else 0, "render_order": "default",
                         "from": [x0, y0, z0], "to": [x1, y1, z1],
                         "origin": [(x0+x1)/2, (y0+y1)/2, (z0+z1)/2],
                         "rotation": [0, 0, 0], "faces": faces, "type": "cube", "uuid": element_id})

    geo_bones = [{"name": "root", "pivot": [0, 0, 0]}]
    outliner = []
    nodes = {}
    for bone in spec.get("parents", {}):
        if bone != "root":
            groups.setdefault(bone, {"uuid": uid(key, "bone", bone), "children": []})
    for name, group in groups.items():
        member_boxes = [entries[i]["box"] for i, e in enumerate(entries) if e["group"] == name]
        hinge_boxes=member_boxes
        if not spec.get("authored_bones") and name.endswith("arm"):
            anatomical=[e["box"] for e in entries if e["group"]==name and re.search(r"\barms?\b",e["label"].lower())]
            if anatomical:hinge_boxes=anatomical
        pivot = spec.get("pivots", {}).get(name, group_pivot(name, [(None, *box) for box in hinge_boxes]) if hinge_boxes else [0, 0, 0])
        if not member_boxes and name=="head":
            child_boxes=[e["box"] for e in entries if spec["parents"].get(e["group"])==name]
            if child_boxes:pivot=group_pivot(name,[(None,*box) for box in child_boxes])
        if not spec.get("authored_bones") and key in ("regolith_crawler","rust_beetle","sand_skitter","gildcrab") and name.startswith("leg_") and not name.endswith(("_shin","_foot")):
            pivot[0]=max(b[3] for b in member_boxes) if pivot[0]<0 else min(b[0] for b in member_boxes)
        group["pivot"] = pivot
        nodes[name] = {"name": name, "origin": pivot, "color": 0, "uuid": group["uuid"],
                         "export": True, "isOpen": False, "locked": False,
                         "visibility": True, "children": list(group["children"])}
        if name in spec.get('rotations',{}):nodes[name]['rotation']=spec['rotations'][name]
        cubes = []
        for i, entry in enumerate(entries):
            if entry["group"] != name:
                continue
            x0,y0,z0,x1,y1,z1 = entry["box"]
            faces = elements[i]["faces"]
            uv = {face: {"uv": data["uv"][:2],
                          "uv_size": [data["uv"][2]-data["uv"][0], data["uv"][3]-data["uv"][1]]}
                  for face, data in faces.items()}
            cubes.append({"origin": [x0, y0, z0], "size": [x1-x0, y1-y0, z1-z0], "uv": uv})
        if name in spec.get("parents", {}):
            parent = spec["parents"][name]
        elif name.endswith("_shin"):
            parent = name.removesuffix("_shin")
        elif name.endswith("_foot"):
            stem = name.removesuffix("_foot")
            parent = stem + "_shin" if stem + "_shin" in groups else stem
        else:
            parent = "head" if (name.endswith("ear") or name in ("antlers","jaw","mouth")) and "head" in groups else "neck" if name=="head" and "neck" in groups else "body" if name not in ("body", "orbit", "corona") else "root"
        if parent not in groups:
            parent = "root"
        group["parent"] = parent
        geo_bones.append({"name": name, "parent": parent, "pivot": pivot, "cubes": cubes})
        if name in spec.get('rotations',{}):geo_bones[-1]['rotation']=spec['rotations'][name]
    root_node = {"name": "root", "origin": [0, 0, 0], "uuid": uid(key, "root"),
                 "export": True, "visibility": True, "children": []}
    for name, node in nodes.items():
        parent = groups[name]["parent"]
        (root_node if parent == "root" else nodes[parent])["children"].append(node)
    outliner = [root_node]

    base_path = assets / "textures/entity" / f"{key}.png"
    glow_path = assets / "textures/entity" / f"{key}_glowmask.png"
    base_path.parent.mkdir(parents=True, exist_ok=True)
    base.save(base_path)
    if glow.getbbox():
        glow.save(glow_path)
    elif glow_path.exists():
        glow_path.unlink()

    data = io.BytesIO()
    base.save(data, format="PNG")
    source = "data:image/png;base64," + base64.b64encode(data.getvalue()).decode("ascii")
    texture = {"path": str(base_path), "name": base_path.name, "folder": "entity",
               "namespace": namespace, "id": "0", "particle": False,
               "visible": True, "mode": "bitmap", "saved": True,
               "uuid": uid(key, "texture"), "source": source}
    animation_groups = {**groups, "root": {"uuid": root_node["uuid"], "pivot": [0, 0, 0]}}
    if spec.get("authored_bones"):
        from build_shattered_models import animate_rig
        bb_animations, gecko_animations = animate_rig(key, spec["base_rig"], animation_groups)
    else:
        bb_animations, gecko_animations = animations_for(key, animation_groups)
    eye_groups={n:g for n,g in groups.items() if n.startswith("eye_")}
    eye_actions=("blink","look_left","look_right") if eye_groups else ("core_pulse",)
    for action in eye_actions:
        length=.24 if action=="blink" else 1.2
        animators={}
        export={}
        targets=eye_groups if eye_groups else {n:g for n,g in groups.items() if n in ("core","body","head")}
        if action in ('look_left','look_right'):
            # Turn a real anatomical head/helm, never slide the entire decal
            # through the cheek. Pupil-only gaze requires runtime UV controls.
            targets={n:g for n,g in groups.items() if n in ('head','helm') and g.get('children')}
        for name,g in targets.items():
            channel="scale" if action in ("blink","core_pulse") else "rotation"
            values=([(0,[1,1,1]),(.08,[1,.02,1]),(.14,[1,.02,1]),(.24,[1,1,1])] if action=="blink"
                    else [(0,[1,1,1]),(.6,[1.04,1.04,1.04]),(1.2,[1,1,1])] if action=="core_pulse"
                    else [(0,[0,0,0]),(.3,[0,8 if action=="look_left" else -8,0]),(.9,[0,8 if action=="look_left" else -8,0]),(1.2,[0,0,0])])
            animators[g["uuid"]]={"name":name,"type":"bone","keyframes":[keyframe(t,channel,v,f"{key}/{action}/{name}") for t,v in values]}
            export[name]={channel:{str(t):v for t,v in values}}
        clip=f"animation.{namespace}.{key}.{action}"
        bb_animations.append({"uuid":uid(key,action),"name":clip,"loop":"loop" if action=="core_pulse" else "once","override":False,"length":length,"snapping":100,"animators":animators})
        gecko_animations["animations"][clip]={"loop":action=="core_pulse","animation_length":length,"bones":export}
    if "jaw" in groups or "mouth" in groups:
        clip=f"animation.{namespace}.{key}.mouth_open"
        animators={};export={}
        for name in ("jaw","mouth"):
            if name not in groups:continue
            channel="rotation" if name=="jaw" else "position"
            target=[20,0,0] if name=="jaw" else [0,-.3,0]
            values=[(0,[0,0,0]),(.2,target),(.6,target),(.8,[0,0,0])]
            animators[groups[name]["uuid"]]={"name":name,"type":"bone","keyframes":[keyframe(t,channel,v,clip+name) for t,v in values]}
            export[name]={channel:{str(t):v for t,v in values}}
        bb_animations.append({"uuid":uid(key,"mouth_open"),"name":clip,"loop":"once","override":False,"length":.8,"snapping":100,"animators":animators})
        gecko_animations["animations"][clip]={"loop":False,"animation_length":.8,"bones":export}
    bb = {"meta": {"format_version": "4.10", "model_format": "geckolib_model", "box_uv": False},
          "name": key, "model_identifier": f"{namespace}:{key}",
          "resolution": {"width": atlas, "height": atlas}, "elements": elements,
          "outliner": outliner, "textures": [texture], "animations": bb_animations}
    geo = {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": f"geometry.{namespace}.{key}",
                        "texture_width": atlas, "texture_height": atlas,
                        "visible_bounds_width": max(2, math.ceil(max(max(e["box"][a+3] for e in entries)-min(e["box"][a] for e in entries) for a in (0,2))/16)+1),
                        "visible_bounds_height": max(2, math.ceil((max(e["box"][4] for e in entries)-min(e["box"][1] for e in entries))/16)+1),
                        "visible_bounds_offset": [(min(e["box"][a] for e in entries)+max(e["box"][a+3] for e in entries))/32 for a in range(3)]},
        "bones": geo_bones}]}
    scale_meta=scale_guardian(key,bb,geo,gecko_animations)
    write_json(projects / f"{key}.bbmodel", bb)
    write_json(assets / "geo" / f"{key}.geo.json", geo)
    write_json(assets / "animations" / f"{key}.animation.json", gecko_animations)
    return {"model": key, "boxes": len(entries), "eye_controls":len(eye_groups),"eye_animation":list(eye_actions),"planes":sum(e["plane_axis"] is not None for e in entries), "texels_per_unit":round(SCALE/scale_meta.get('geometry_multiplier',1),3),"bones": len(groups), "atlas": atlas,
            'scale':scale_meta,
            "emissive": bool(glow.getbbox()), "source_sheet": f"sheets/mobs/*_{key}.png",
            "current_reference":f"previews/{key}.png", "design_override":"Silverfish-inspired low segmented arthropod" if key=="dune_burrower" else "HD facial and rig refinement"}


def scale_guardian(key,bb,geo,animations):
    """Repository guardian rule only; bake scale once, never scale the atlas.

    Hitbox 3.6 x 10.8 is a gameplay rectangle, not a request to squash wide
    anatomical models. Preserve proportions while setting total model height.
    """
    if key not in ('prism_sentinel','rift_tyrant','eidolon_captain','dying_star'):
        return {'rule':'authored size retained'}
    low=min(e['from'][1] for e in bb['elements']);high=max(e['to'][1] for e in bb['elements'])
    factor=172.8/(high-low)
    def point(v):return [round(v[0]*factor,6),round((v[1]-low)*factor,6),round(v[2]*factor,6)]
    for e in bb['elements']:
        for field in ('from','to','origin'):e[field]=point(e[field])
    def nodes(items):
        for n in items:
            if isinstance(n,dict):n['origin']=point(n['origin']);nodes(n['children'])
    nodes(bb['outliner'])
    for clip in bb['animations']:
        for animator in clip['animators'].values():
            for k in animator['keyframes']:
                if k['channel']=='position':
                    for p in k['data_points']:
                        for axis in ('x','y','z'):p[axis]=str(float(p[axis])*factor)
    document=geo['minecraft:geometry'][0]
    for bone in document['bones']:
        bone['pivot']=point(bone['pivot'])
        for cube in bone.get('cubes',[]):
            cube['origin']=point(cube['origin']);cube['size']=[round(v*factor,6) for v in cube['size']]
    description=document['description']
    description['visible_bounds_width']*=factor;description['visible_bounds_height']*=factor
    description['visible_bounds_offset']=[v/16 for v in point([v*16 for v in description['visible_bounds_offset']])]
    for clip in animations['animations'].values():
        for bone in clip['bones'].values():
            for t,v in bone.get('position',{}).items():bone['position'][t]=[float(a)*factor for a in v]
    return {'rule':'repository guardian: 6x player height','height_blocks':10.8,'hitbox_blocks':[3.6,10.8],
            'geometry_multiplier':factor,'scale_baked':True,'runtime_hitbox_pending':True}


def main() -> None:
    manifest = [build(key, spec) for key, spec in {**MOBS, **M2}.items()]
    write_json(PROJECTS / "manifest.json", {"source": "mobs_data.py + mobs_food.py",
                                               "minecraft": "1.21.1", "models": manifest})
    print(f"Built {len(manifest)} Blockbench/GeckoLib mob sets: {sum(m['boxes'] for m in manifest)} boxes")


if __name__ == "__main__":
    main()
