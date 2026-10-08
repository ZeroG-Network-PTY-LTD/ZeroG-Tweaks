"""Generate reference layers and Codex-ready coordinates from the audited layout.

This mirrors SurvivalGateLayout.parts; review the generator whenever that changes.
No crafting costs are invented. Includes overwritten coordinates only once.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

FRAMES = ['nullifite', 'moonsteel', 'cerulite', 'skarnite', 'eidolite', 'solvanite']
SYMBOLS = {f'{name}_gate_frame': str(i+1) for i, name in enumerate(FRAMES)}
SYMBOLS.update(gate_pad_plate='P', gate_pylon='Y', gate_energy_port='E', gate_controller='C', gate_lens_housing='L', selenite_block='S', aresite_block='A')

def parts(tier):
    result = {}
    for t in range(1, tier+1):
        r = t+1
        for x in range(-r, r+1):
            for z in range(-r, r+1):
                if max(abs(x), abs(z)) == r:
                    result[x, -1, z] = FRAMES[t-1]+'_gate_frame'
    pad = 3 if tier >= 5 else 2 if tier >= 3 else 1
    for x in range(-pad, pad+1):
        for z in range(-pad, pad+1):
            if not (abs(x) == 2 and abs(z) == 2): result[x, 0, z] = 'gate_pad_plate'
    for t in range(1, tier+1):
        r = t+1
        if t in (1, 3, 5):
            for x in (-r, r):
                for z in (-r, r):
                    for y in range(tier+2): result[x, y, z] = 'gate_pylon'
        if t >= 2:
            h = t*2
            for x in (-r+1, r-1):
                for y in range(1, h): result[x, y, r] = FRAMES[t-1]+'_gate_frame'
            for x in range(-r+1, r): result[x, h, r] = FRAMES[t-1]+'_gate_frame'
            result[0, h+1, r] = 'gate_lens_housing'
    if tier >= 2:
        result[0, 6, 3] = 'selenite_block'
        result[0, -2, 0] = 'aresite_block'
    result[2, 1, 0] = 'gate_energy_port'
    if tier >= 3: result[-2, 1, 0] = 'gate_energy_port'
    if tier >= 5:
        result[0, 1, 3] = result[0, 1, -3] = 'gate_energy_port'
    result[0, 1, -2] = 'gate_controller'
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--docs', type=Path, required=True)
    a=p.parse_args()
    source=Path(__file__).resolve().parents[1]/'src/main/java/net/zerog/tweaks/travel/SurvivalGateLayout.java'
    manifest={'schema':2,'source':'SurvivalGateLayout.parts','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(), 'formation_sha256':hashlib.sha256(source.with_name('SurvivalGateFormation.java').read_bytes()).hexdigest(), 'coordinate_system':'north-facing example; centre pad level is y=0; structural front is negative Z; terminal facing is cosmetic', 'tiers':[]}
    text=['# Concord gates — exact tier 1–6 construction guide', '',
          'Minecraft 1.21.1 · same 1.0.12-dev · runtime construction, not proposed concept art.', '',
          '## Reading the plans', '',
          'Choose a centre **(X, Y, Z)**. Y is the pad-block level, not the foundation. All positions below are relative to that centre. For a north-facing structural example, front is −Z and the example controller is at **(0, +1, −2)**. Foundations occupy y=−1; tier 2+ also has Aresite at y=−2. Reserve a square `(2×tier+3)` blocks wide, from x/z `−(tier+1)` to `+(tier+1)`. Highest required layer: tier 1 y=2; tier 2 y=6; tiers 3–6 y=`2×tier+1`.', '',
          'Rotate structural coordinates for another orientation: EAST `(−z,y,x)`, SOUTH `(−x,y,−z)`, WEST `(z,y,−x)`. The controller front does not rotate or determine the structure. Choose service positions independently under the rule below.', '',
          'Layer diagrams are viewed from above: north/−Z at the top; X increases to the right. Each character represents one block at that layer. `.` means no required part, not an instruction to fill it. Keep the passenger area unobstructed.', '',
          'Legend: `1` Nullifite Frame; `2` Moonsteel Frame; `3` Cerulite Frame; `4` Skarnite Frame; `5` Eidolite Frame; `6` Solvanite Frame; `P` Gate Pad Plate; `Y` Gate Pylon; `E` Gate Energy Port; `C` Gate Controller; `L` Gate Lens Housing; `S` Selenite Block; `A` Aresite Block.', '',
          '**Landing Platform blocks are optional landscaping, not formation requirements.** The compact hub uses them only under gate footprints. Frame rings must remain the specified gate-frame blocks, not Landing Platforms.', '',
          '## Order of construction', '',
          '1. Excavate the foundation and buried core position; build each concentric frame ring at y=−1.',
          '2. Place the pad plates at y=0, retaining the four omitted `(±2,0,±2)` positions where the tier plan omits them.',
          '3. Build the four pylon columns for each active pylon ring. Existing inner columns grow taller when upgrading.',
          '4. Add the rear frame arches, their lens housings, and tier-2+ Selenite/Aresite blocks exactly as drawn.',
          '5. Install exactly one controller and at least 1/1/2/2/4/4 Gate Energy Ports for tiers 1–6. Service blocks may occupy any horizontal side at y=1 where max(abs(x),abs(z)) is between 2 and tier+1, without replacing a structural part. Controller facing is cosmetic. C/E positions in these diagrams are valid examples, not mandatory sockets. Connect power to a **Gate Energy Port**, not a generic alveary port.',
          '6. Open the controller, check its formed tier, choose a reachable destination and supply FE for survival travel. Preview can highlight missing next-tier blocks.', '',
          'A higher tier retains earlier rings/arches but changes pylon heights and pad/port positions. Use the full target-tier plan; simply adding an outer ring is insufficient. Counts below describe the complete final structure, not additive shopping lists.', '']
    bases=[500000,1000000,3000000,8000000,20000000,50000000]
    for tier in range(1,7):
        layout=parts(tier); counts=dict(sorted(collections.Counter(layout.values()).items())); r=tier+1
        structural={pos:block for pos,block in layout.items() if block not in ('gate_controller','gate_energy_port')}
        services=[[x,1,z] for x in range(-r,r+1) for z in range(-r,r+1) if max(abs(x),abs(z))>=2 and (x,1,z) not in structural]
        manifest['tiers'].append({'tier':tier,'counts':counts,'parts_are_default_example':True,'controller_count':1,'minimum_energy_ports':1 if tier<3 else 2 if tier<5 else 4,'legal_service_offsets':services,'parts':[{'offset':list(pos),'block':'zerog_tweaks:'+block} for pos,block in sorted(layout.items())]})
        text.extend([f'## Tier {tier} — {FRAMES[tier-1].title()}', '', f'Footprint **{2*r+1}×{2*r+1}**; required blocks **{len(layout)}**. Default base travel budget **{bases[tier-1]:,} FE**.', '', '| Required block ID | Count |', '| --- | ---: |'])
        text.extend(f'| `zerog_tweaks:{name}` | {count} |' for name,count in counts.items())
        for y in sorted({pos[1] for pos in layout}):
            text.extend(['', f'### Layer y={y:+d}', '', '```text'])
            for z in range(-r,r+1): text.append(''.join(SYMBOLS[layout[x,y,z]] if (x,y,z) in layout else '.' for x in range(-r,r+1)))
            text.append('```')
        text.append('')
    text.extend(['## Activation, power and passenger rules', '',
        '| Tier | Normal destination ceiling | Passenger limit | Energy ports | Upgrade slots | Intake FE/tick | Default buffer FE |', '| --- | --- | ---: | ---: | ---: | ---: | ---: |'])
    ceilings=['Galaxy 1: Overworld, Moon and Mars','Galaxy 2, including Cerulon','Galaxy 3, including Skarn','Galaxy 4, including Eidolon','Galaxy 5, including Solvane; grouped moon destinations excluded','Galaxy 5 plus grouped `g*_moons` destinations']
    for t in range(1,7): text.append(f'| {t} | {ceilings[t-1]} | {2 if t<3 else 4 if t<5 else 8} | {1 if t<3 else 2 if t<5 else 4} | {1 if t<3 else 2 if t<5 else 3 if t<6 else 4} | {1000 << (t-1):,} | {bases[t-1]*2:,} |')
    text.extend(['',
        'Player jumps cost exactly **100,000 / 200,000 / 400,000 / 800,000 / 1,600,000 / 3,200,000 FE** at tiers1–6. One successful group jump is charged once; no intra-galaxy, passenger or lens factor applies. Cancelled/invalid launches do not consume FE. Existing stored energy is preserved. Recall item fees remain separate.', '',
        'Gate upgrades: **Refracting Lens** remains recoverable but does not discount the fixed jump tariff; **Cryo Core** doubles intake rate; **Capacity Coil** adds two passengers; **Star Map Fragment** is accepted in a gate upgrade socket, but this guide does not claim an additional undocumented effect. These are gate-specific items, not general machine Acceleration cards.', '',
        'Open the controller, choose **Plans**, then Tier1–6. The standing wireframe is anchored to this controller: green correct, cyan missing, red mismatched. Choosing a preview never builds blocks or changes the formed tier. Above the terminal, a transient galaxy/planet hologram shows live FE and countdown; gate dimension travel activates the existing transition artwork.', '',
        'The first interaction claims a normal controller for its owner. Stand above the pad, choose the destination, launch, and have each passenger confirm Ready. The sequence lasts 100 ticks (~5 seconds). Leaving the pad, excessive passengers, an invalid destination or broken formation cancels it. Real travel builds/reuses a bound return platform at the destination; there is no need to pre-build every planetary gate.', '',
        '**Lore versus current validation:** guardian keys are existing story/loot objects. `SurvivalGateLayout`/`SurvivalGateBlockEntity` validate physical tier, ownership, readiness and FE; they do not consume four keys from a survival-controller key inventory. Do not write a Codex instruction claiming that unverified mechanic is implemented. Track any intended key-activation contract separately.', '',
        '## Compact hub inspection coordinates', '',
        'The six showcase gates have admin/free travel as requested. They still use real tier geometry. Their zero FE cost and unrestricted destinations are a deliberate hub-only bypass, not a survival balance change.', '',
        '| Tier | Pad centre | Controller |', '| --- | --- | --- |'])
    for t in range(1,7):
        x=-22+((t-1)%3)*22; z=-22-((t-1)//3)*22
        text.append(f'| {t} | `{x},64,{z}` | `{x},65,{z-2}` |')
    text.extend(['', '## Troubleshooting and Codex handoff', '',
        '- Tier reads zero: press Preview for missing blocks grouped by section, or Ghost for a temporary wireframe. Align rechecks without rotating the terminal or supplying blocks. Check buried core, ring material, pylon height, arch top, lens location and legal service-block counts. Chunks containing the full footprint must be loaded.',
        '- Higher tier not detected: compare **all** layers; earlier pylons must reach the new height and the target tier needs its minimum number of legal ports.',
        '- No charging: required Gate Energy Ports must occupy legal service positions even when powering the controller directly. A formed port and controller share one buffer; duplicate controllers and ports shared between complete gates are rejected. Check cable/generator output faces and available generation. Exact stored FE is synchronized; full admin buffers do not accept extra charge.',
        '- Cannot launch: inspect ownership, reachable tier, energy cost, passenger limit and Ready confirmations.',
        '- A normal survival gate showing free travel is not expected. Only designated compact-hub controllers and their bound returns are admin.', '',
        'The companion [coordinate manifest](gate-build-layouts-1.21.1.json) records every required block once, exact IDs/counts and the audited source hash for future localized Codex pages. Re-run the generator and review it whenever the layout source changes. This does not finalize deferred survival crafting ingredient costs.', ''])
    root=a.docs/'docs'; root.mkdir(exist_ok=True)
    (root/'gate-building-tiers-1.21.1.md').write_text('\n'.join(text), encoding='utf-8')
    (root/'gate-build-layouts-1.21.1.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({str(t['tier']):t['counts'] for t in manifest['tiers']},indent=2))

if __name__=='__main__': main()
