"""Illustrated Concord field guide. Native block/item renders, no invented recipes or story unlocks.

Called LAST by write_guide.py. Gate geometry comes from the audited code helper;
the Java GameTest compares every depicted layer against real SurvivalGateLayout.parts.
"""
from pathlib import Path
import importlib.util
from collections import Counter

def enhance(asset_root):
    assets=Path(asset_root).resolve(); code=assets.parents[4]
    spec=importlib.util.spec_from_file_location('gate_layout',code/'tools/generate_gate_build_guide.py')
    layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
    guide=assets/'guides/zerog_tweaks/concord_codex'
    def page(name,title,icon,pos,body,parent='index.md'):
        (guide/name).write_text(f'---\nnavigation:\n  title: "{title}"\n  icon: {icon}\n  position: {pos}\n  parent: {parent}\n---\n\n{body}\n',encoding='utf-8')
    def scene(parts,zoom=2):
        return '\n'.join([f'<GameScene zoom="{zoom}" interactive={{true}}>']+
          [f'  <Block id="zerog_tweaks:{block}" x="{x}" y="{y}" z="{z}" />' for (x,y,z),block in sorted(parts.items())]+
          ['  <IsometricCamera yaw="195" pitch="30" />','</GameScene>'])
    def row(names):
        return '<Row>\n'+'\n'.join(f'  <ItemImage id="zerog_tweaks:{name}" scale="3" />' for name in names)+'\n</Row>'
    index=guide/'index.md'
    index.write_text('''---
navigation:
  title: Concord Field Journal
  icon: zerog_tweaks:concord_codex
  position: 0
---

# The Concord Field Journal

> Earth was our refuge. The Pathfinder never reached the surface. Deep beneath your feet, its broken heart still hums.

## Begin with a signal, not a shopping list

'''+row(['raw_nullifite','dormant_wisp','concord_codex'])+'''

1. **Listen:** recover Raw Nullifite with the correct pickaxe.
2. **Answer:** find the Courier, recover Echo and read the Broken Console.
3. **Build:** follow the foundation, pad, service row and pylon diagrams.
4. **Remember:** travel to the Moon and Mars. Later memories open only after your own arrivals and milestones.

Right-click opens your personal illustrated journal. Its checkboxes are server-recorded milestones, not clickable rewards. Sneak-right-click preserves the native story book. The **Field guide** is a public technical reference; its construction pages do not unlock sealed personal memories.

## Expedition desk

- [Gate construction atlas — every layer, tiers 1–6](16_gate_atlas.md)
- [Machine fieldbook — purpose, power and recipe controls](17_machine_fieldbook.md)
- [Comets and asteroids — what to mine and what to avoid](18_impacts.md)

## Follow the story

**Prologue / The Signal:** [Listen](01_signal.md) → [Build](02_gate.md) → [Power](03_power.md) → [Launch](04_launch.md).

**Act I / The Falling Star:** [Moon relay](05_moon.md) → [Mars waystation](06_mars.md) → [Mining ladder](07_mining.md) → [Return home](08_home.md).

**Beyond the waystation:** [Tier 2](09_tier2.md) → [Planetary exploration](10_planet_exploration.md). Your personal journal carries the later recovered memories; unfinished encounters and research rules are not promises of working gameplay.

## Reference shelves

<SubPages />
''',encoding='utf-8')
    page('16_gate_atlas.md','Construction / Gates 1–6','zerog_tweaks:gate_controller',160,
      '# Gate construction atlas\n\n'+row(['gate_controller','gate_energy_port','gate_pad_plate'])+
      '\n\nChoose a tier below. Each picture is **one horizontal layer**, viewed in 3D; drag to turn it. Pad level is y=0. Build from the buried foundation upwards. Empty cells are not filler blocks.\n\n'+
      '\n'.join(f'- [Tier {t} / {layout.FRAMES[t-1].title()}](gate_t{t}.md)' for t in range(1,7))+
      '\n\nController facing is cosmetic. Use exactly one controller and at least 1/1/2/2/4/4 Gate Energy Ports. Services sit one block above the pad, on any horizontal side in the legal service area, never in place of a structural part. Diagram service positions are examples.\n\nUse controller **Plans → Plan T1–T6** for the standing hologram; **Build T1–T6** checks and consumes carried missing blocks. Neither guide pictures nor preview supply free materials.\n\nSurvival jumps cost 100,000 FE at T1, doubling each tier to 3,200,000 FE at T6. Admin gates are separate. Higher galaxy moons open at their galaxy tier.\n\n[Power and charging](03_power.md) · [Ready and launch](04_launch.md).')
    for t in range(1,7):
        parts=layout.parts(t);count=Counter(parts.values()); r=t+1
        body=f'# Tier {t} / {layout.FRAMES[t-1].title()}\n\nFootprint {2*r+1} × {2*r+1}; complete target layout, not an additive shopping list. Jump: {100000 << (t-1):,} FE. Earlier columns must grow to the target height.\n\n'
        body+='| Block | Required |\n| --- | ---: |\n'+'\n'.join(f'| <ItemLink id="zerog_tweaks:{block}" /> | {n} |' for block,n in sorted(count.items()))+'\n\n'
        for number,y in enumerate(sorted({p[1] for p in parts}),1):
            cells={ (x+r,yy+2,z+r):block for (x,yy,z),block in parts.items() if yy==y }
            meaning='Buried core' if y==-2 else 'Foundation rings' if y==-1 else 'Pad and column feet' if y==0 else 'Services / columns / rear arch'
            body+=f'## Step {number} / Layer y={y:+d} — {meaning}\n\n'+scene(cells,1.6)+'\n\n'
        body+='## Final check\n\n'+scene({(x+r,y+2,z+r):b for (x,y,z),b in parts.items()},1.6)+f'\n\nOpen the controller and **Align**. Missing parts are grouped by structural section. Connect generation to a Gate Energy Port and verify the shared FE buffer before launch. [Back to the atlas](16_gate_atlas.md).'
        page(f'gate_t{t}.md',f'Tier {t} / {layout.FRAMES[t-1].title()}',f'zerog_tweaks:{layout.FRAMES[t-1]}_gate_frame',t*10,body,'16_gate_atlas.md')
    machines=[('ore_refinery','Ore Refinery','Ore processing. Use the loaded recipe page for quantities, catalyst identity and outputs.'),
      ('alloy_forge','Alloy Forge','Combine the required inputs. Check whether the chosen recipe consumes or retains its catalyst.'),
      ('crystal_growth_chamber','Crystal Growth Chamber','Supply the recipe seed and feed; leave output room.'),
      ('salvage_station','Salvage Station','Recover listed salvage. Chance-based results are not guaranteed.'),
      ('combustion_generator','Combustion Generator','Fuel, burn progress and FE output. Dusts are not combustion fuels.'),
      ('solar_array','Solar Array','No fuel slot: daylight and sky access produce FE. It outputs power; it does not need incoming FE.'),
      ('fusion_reactor','Fusion Reactor','Existing Fusion Dust fuel route. No unapproved gas or liquid reactor route is implied.')]
    body='# The expedition workshop\n\nRead the terminal, then wire the machine. Artwork alone is not a recipe.\n\n'
    for ident,title,purpose in machines:
        body+=f'## {title}\n\n<BlockImage id="zerog_tweaks:{ident}" scale="3" />\n\n{purpose}\n\n<ItemLink id="zerog_tweaks:{ident}" />\n\n'
    body+='## Before pressing Start\n\n1. Open **Items / Recipes**. Read every input quantity, alternative and catalyst rule.\n2. Set item/fluid/power faces to supported input or output roles. A visible connector alone is not proof of transfer.\n3. Check FE and output space. Recipe browsing never processes or moves items.\n4. Consult **Upgrades**: compatibility is machine-specific; generator Flux Modules are not Acceleration cards.\n\n[Genetics](11_genetics.md) · [Generators](12_generators.md) · [Alvearies](13_alveary_recipes.md) · [Frames](14_frame_recipes.md) · [Stardust Smelter](15_stardust_smelter.md).'
    page('17_machine_fieldbook.md','Workshop / Machine fieldbook','zerog_tweaks:alloy_forge',170,body)
    shell={}
    # Exact integer sphere section from CometRemnant.cells, y=4; palette illustration, not a guaranteed loot roll.
    for x in range(10):
        for z in range(10):
            d=(2*x-9)**2+(-1)**2+(2*z-9)**2
            if d<=100:shell[x,0,z]='eclipse_opal_ore' if d<=3 else 'moonsteel_ore' if d<=11 else 'meteorite_fragment' if d<=49 else 'lunar_stone'
    page('18_impacts.md','Exploration / Comets and asteroids','zerog_tweaks:meteorite_fragment',180,
      '# A falling light, a buried reward\n\n'+row(['meteorite_fragment','stardust','star_map_fragment'])+
      '\n\nThe Concord Courier is a story event: Echo and the Codex wait inside its pod. Ordinary planetary comets and asteroids are different events. Static Impact Site ruins are different again. Do not expect a Dormant Wisp in every crater.\n\n## Read the remnant\n\n'+scene(shell,2)+
      '\n\n**Cutaway illustration:** one middle slice through the actual 10-block spherical remnant. Outer rock protects a fragment-rich mantle and rarer central ore/gems. This Moon palette picture explains layers, not guaranteed ore counts; materials and random inclusions vary by planet. Mine inward with the correct tool.\n\n## Field notes\n\n- Impacts are limited to one successful event per active planet per Minecraft day (24,000 ticks), with players present and suitable loaded terrain. Placement can fail; an impact is not guaranteed at a particular time or spot.\n- The event searches after day-time 18,000 and reports its X/Z. Terrain is excavated; do not stand in the strike area. Arrival protection prevents impacts cutting into a protected landing footprint.\n- Moon impacts can bring a Meteor Maw; that is not guaranteed, and Peaceful suppresses it. Star Map Fragments are existing lore carriers. A small Maw wreck narrative remains pending—no Broken Console mob drop is promised.\n- Ocean impacts can reach the seabed. Bring appropriate equipment; admin spectator inspection is not survival safety.\n\n[Planetary exploration](10_planet_exploration.md) · [Mining ladder](07_mining.md).')
    # Keep current facts, but add consistent visual entry points to existing chapters.
    icons={'01_signal.md':['hull_plating','broken_console','dormant_wisp'],
      '03_power.md':['combustion_generator','gate_energy_port','gate_controller'],
      '04_launch.md':['gate_controller','gate_pad_plate','capacity_coil'],
      '07_mining.md':['nullifite_pickaxe','ferrox_pickaxe','moonsteel_pickaxe'],
      '09_tier2.md':['moonsteel_gate_frame','selenite_block','aresite_block']}
    for name,names in icons.items():
        path=guide/name;source=path.read_text(encoding='utf-8');split=source.index('\n',source.index('\n# ')+1)
        path.write_text(source[:split]+'\n\n'+row(names)+source[split:],encoding='utf-8')
    print('Illustrated journal: six complete gate atlases, machine fieldbook and remnant cutaway.')
