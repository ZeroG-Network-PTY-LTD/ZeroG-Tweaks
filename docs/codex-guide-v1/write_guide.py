"""Concord Codex GuideME pages (v1): the Sol loop walkthrough.

usage: python write_guide.py <code-branch src/main/resources/assets/zerog_tweaks dir>
Writes guideme_guides/concord_codex.json and guides/zerog_tweaks/concord_codex/*.md. Facts come from the
1.21.x code (SurvivalGateLayout, SurvivalGateBlockEntity, CombustionBlockEntity, ZGProgressionConfig,
ConcordPrologue, needs_*_tool tags); update this script when those change.
"""
import os
import sys
A = sys.argv[1]
G = A + "/guides/zerog_tweaks/concord_codex"
os.makedirs(G, exist_ok=True)
os.makedirs(A + "/guideme_guides", exist_ok=True)

# T1 layout from travel/SurvivalGateLayout.parts(1), shifted by +2 so every coordinate is >= 0.
scene = []
for x in range(5):
    for z in range(5):
        if max(abs(x - 2), abs(z - 2)) == 2:
            scene.append(f'  <Block id="zerog_tweaks:nullifite_gate_frame" x="{x}" y="0" z="{z}" />')
for x in range(1, 4):
    for z in range(1, 4):
        scene.append(f'  <Block id="zerog_tweaks:gate_pad_plate" x="{x}" y="1" z="{z}" />')
for x in (0, 4):
    for z in (0, 4):
        for y in (1, 2, 3):
            scene.append(f'  <Block id="zerog_tweaks:gate_pylon" x="{x}" y="{y}" z="{z}" />')
scene.append('  <Block id="zerog_tweaks:gate_energy_port" x="4" y="2" z="2" />')
scene.append('  <Block id="zerog_tweaks:gate_controller" x="2" y="2" z="0" />')
SCENE = "\n".join(scene)

with open(A + "/guideme_guides/concord_codex.json", "w", newline="\n") as f:
    f.write('{\n  "item_settings": {\n    "display_name": { "translate": "item.zerog_tweaks.concord_codex" },\n'
            '    "model": "zerog_tweaks:item/concord_codex"\n  },\n  "default_language": "en_us"\n}\n')


def page(name, title, icon, pos, body, parent="index.md", items=None):
    fm = f"---\nnavigation:\n  title: {title}\n  icon: {icon}\n  position: {pos}\n"
    if parent:
        fm += f"  parent: {parent}\n"
    if items:
        fm += "item_ids:\n" + "".join(f"  - {i}\n" for i in items)
    with open(f"{G}/{name}", "w", newline="\n", encoding="utf-8") as f:
        f.write(fm + "---\n\n" + body.strip() + "\n")


def link(i):
    return f'<ItemLink id="zerog_tweaks:{i}" />'


page("index.md", "Concord Codex", "zerog_tweaks:concord_codex", 0, parent=None, body="""
# Concord Codex

> *Earth was our refuge. Our Pathfinder crashed deep in its rock. Its gate core became the humming Nullifite.*

This book walks you through **Sol**, the first part of ZeroG: from your first Nullifite to building a gate,
travelling to the Moon and Mars, and getting home again. Read the pages in order the first time.
Click any item name to jump to its page. Recipes shown here are always the live, current ones.

**Sneak and right-click** the Codex to read Echo's story pages instead. New pages appear as you reach new worlds.

## Your task journal

Sneak and right-click also opens your personal task list first: **[x]** is a recorded
milestone and **[ ]** is outstanding. Reopen the book to refresh it. Later planetary
task pages remain sealed until you have arrived there; reading this guide never grants
progress. Follow the chapter links below for the diagrams and practical steps.

<SubPages />
""")

page("01_signal.md", "1. The Signal", "zerog_tweaks:raw_nullifite", 10,
     items=["zerog_tweaks:dormant_wisp", "zerog_tweaks:broken_console", "zerog_tweaks:raw_nullifite"], body=f"""
# 1. The Signal

<Row>
  <BlockImage id="zerog_tweaks:deepslate_nullifite_ore" scale="3" />
  <ItemImage id="zerog_tweaks:raw_nullifite" scale="3" />
</Row>

## Mine Nullifite

* {link("deepslate_nullifite_ore")} is found in deepslate from **Y -64 to -40**.
* The **Deep Dark** has a lot more of it. Ancient cities sit right in that band.
* You need a **Netherite pickaxe** to mine it.

## The Courier

1. Pick up your first {link("raw_nullifite")}. A message says a relay is listening.
2. Be in the **Overworld at night**. A Concord Courier pod crashes **48 to 96 blocks** from you,
   and chat gives you its **X and Z**.
3. Open the chest in the pod. It holds the {link("dormant_wisp")} and this Codex.
   Right-click the {link("broken_console")} for the Concord's message.

**Lost the Wisp?** If you have no Wisp and no Gate Controller **7 days** after the first pod, a backup pod falls.
Ancient city chests also have a small chance to hold a Dormant Wisp.

Next: [build the gate](02_gate.md).
""")

page("02_gate.md", "2. Build the T1 Gate", "zerog_tweaks:gate_controller", 20,
     items=["zerog_tweaks:gate_controller", "zerog_tweaks:nullifite_gate_frame", "zerog_tweaks:gate_pad_plate",
            "zerog_tweaks:gate_pylon", "zerog_tweaks:gate_energy_port"], body=f"""
# 2. Build the T1 Gate

The gate is a multiblock. This is the whole Tier 1 build. Drag to rotate, scroll to zoom.

<GameScene zoom="4" interactive={{true}}>
{SCENE}
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Parts list

| Part | Count | Where it goes |
| --- | --- | --- |
| {link("nullifite_gate_frame")} | 16 | A 5x5 ring, one layer **below** the pad |
| {link("gate_pad_plate")} | 9 | The 3x3 pad in the middle of the ring |
| {link("gate_pylon")} | 12 | Four corner columns, 3 tall, on the ring's corners |
| {link("gate_controller")} | 1 | Any legal service position, one block above the pad |
| {link("gate_energy_port")} | 1 | Another legal service position on any horizontal side |

**Tip:** open the controller and press **Ghost** to toggle the current-tier wireframe for
60 seconds: green means correct, cyan means missing, and red means the wrong block.
It never places blocks. **Preview** lists required block counts by structural section,
not world coordinates. A complete gate is explicitly marked complete; requirements
for the next tier are labelled an **optional upgrade**, not an alignment error.
**Align** rechecks the structure; it never rotates the terminal or replaces blocks.
Controller facing is cosmetic. Service blocks belong at pad height +1, with
`max(abs(x), abs(z))` between 2 and tier +1, without replacing structural parts.
Use exactly one controller and at least 1/1/2/2/4/4 Gate Energy Ports at tiers 1–6.
The Ghost port positions are recommendations, not mandatory sockets. Ports are
required even when charging the controller directly, and cannot be shared by gates.

## Recipes

The controller is built around the Dormant Wisp from the Courier.

<RecipeFor id="zerog_tweaks:gate_controller" />

<RecipeFor id="zerog_tweaks:nullifite_gate_frame" />

<RecipeFor id="zerog_tweaks:gate_pad_plate" />

<RecipeFor id="zerog_tweaks:gate_pylon" />

<RecipeFor id="zerog_tweaks:gate_energy_port" />

Next: [power it](03_power.md).
""")

page("03_power.md", "3. Power the Gate", "zerog_tweaks:combustion_generator", 30,
     items=["zerog_tweaks:combustion_generator"], body=f"""
# 3. Power the Gate

Gates run on **FE**. The simplest source is a {link("combustion_generator")}.

<RecipeFor id="zerog_tweaks:combustion_generator" />

1. Place the generator **touching the Gate Energy Port**. It pushes power into the blocks next to it.
   Alternatively, connect it with ZeroG energy conduits: generator output to the port.
   The port charges the controller's shared buffer; it has no separate battery.
2. Fuel it. Coal-type fuels give **50 FE/t**; {link("emberite")} gives 100, {link("cryocite")} 150
   and {link("coronite")} 200.

## How much do I need?

| Tier 1 gate | |
| --- | --- |
| Battery | 1,000,000 FE |
| Fastest charging | 1,000 FE/t |
| Tier 1 successful gate jump (any eligible group) | 100,000 FE |
| Each extra passenger | +10% |

At 50 FE/t one Tier 1 trip needs 100 seconds of burning. The controller screen shows the stored FE.

Next: [launch](04_launch.md).
""")

page("04_launch.md", "4. Launch", "zerog_tweaks:gate_pad_plate", 40, body=f"""
# 4. Launch

1. **Right-click the Gate Controller.** The first player to do this owns the gate. Only the owner can launch it.
2. Pick a destination: **moon** or **mars** at Tier 1. Use the arrow buttons to page through the list.
3. Stand on the pad and press **Engage**. A Tier 1 pad carries **2 players**.
4. Everyone on the pad opens the controller and presses **Ready** before the 5-second countdown ends.
   Step off the pad or press **Cancel** to abort.

Tamed pets owned by a passenger, and mobs on a passenger's lead, come along.

## Arriving

Your first trip builds a **landing platform** on the planet: a small gate with a {link("crystal_cell")}
under it. The cell recharges the platform by 1,000 FE every second, so after about 100 seconds you can use
the platform to fly **home** to the gate you left from.

Next: [the Moon](05_moon.md).
""")

page("05_moon.md", "5. The Moon", "zerog_tweaks:moonsteel_ore", 50, body=f"""
# 5. The Moon

> *The Lunari call you the one who answered the signal.*

* **Ores:** {link("moonsteel_ore")}, {link("selenite_ore")} and {link("regolith_ore")}.
* **Biomes:** Lunar Mare, Lunar Highlands and Shadowed Craters.
* **People:** the Lunari. Talk to one after your Courier has landed.
* **Wildlife:** Regolith Crawlers and Moon Hoppers. Meteor Maws arrive with meteor impacts.

Gravity is lower here: jumps go higher and falls are gentler.

Moonsteel needs a **Ferrox pickaxe**, so most players visit [Mars](06_mars.md) first.
""")

page("06_mars.md", "6. Mars", "zerog_tweaks:ferrox_ore", 60, body=f"""
# 6. Mars

> *The Rustborn's hand-cut Aresite core is the first proof the Concord was real.*

* **Ores:** {link("ferrox_ore")}, {link("olympium_ore")} and {link("aresite_ore")}.
* **Biomes:** Rust Plains, Oxide Badlands and the Polar Caps.
* **People:** the Rustborn. Every Rustborn village keeps an Aresite core shrine.
* **Crash sites:** wreckage on the surface with loot chests.

Your Nullifite pickaxe mines **Ferrox**, so start upgrading here. See [the mining ladder](07_mining.md).
""")

page("07_mining.md", "7. Mining Ladder", "zerog_tweaks:nullifite_pickaxe", 70, body=f"""
# 7. Mining Ladder

Each Sol ore needs the pickaxe from the step before it. With a weaker pickaxe the ore breaks but drops nothing.

| Ore | Found on | Needs at least |
| --- | --- | --- |
| {link("deepslate_nullifite_ore")} | Overworld | Netherite pickaxe |
| {link("ferrox_ore")} | Mars | {link("nullifite_pickaxe")} |
| {link("moonsteel_ore")} | Moon | {link("ferrox_pickaxe")} |
| {link("olympium_ore")} | Mars | {link("moonsteel_pickaxe")} |
| {link("selenite_ore")} | Moon | {link("moonsteel_pickaxe")} |
| {link("aresite_ore")} | Mars | {link("olympium_pickaxe")} |

<RecipeFor id="zerog_tweaks:nullifite_pickaxe" />
""")

page("08_home.md", "8. Getting Home", "zerog_tweaks:recall_anchor", 80,
     items=["zerog_tweaks:recall_anchor", "zerog_tweaks:group_anchor"], body=f"""
# 8. Getting Home

There are two ways back:

* **The landing platform** on each planet (see [Launch](04_launch.md)). Free, but it has to recharge.
* **A Recall Anchor**, which works from anywhere.

<RecipeFor id="zerog_tweaks:recall_anchor" />

1. Right-click your **home Gate Controller** with the anchor to bind it.
2. Use the anchor anywhere to jump back to that gate.
3. Recall retains its separate legacy pricing (150% of the old configured travel formula), taken from the home gate's battery, and has a **1-minute** cooldown. It is not the new fixed gate-jump tariff.

The {link("group_anchor")} works the same way and also brings scoreboard teammates within 8 blocks.

<RecipeFor id="zerog_tweaks:group_anchor" />
""")

page("09_tier2.md", "9. Toward Tier 2", "zerog_tweaks:moonsteel_gate_frame", 90, body=f"""
# 9. Toward Tier 2

> *Moonsteel frames, a Selenite lens and this core are the next step toward the Quiet Mines.*

A Tier 2 gate is built **around** your Tier 1 gate. Keep everything and add:

* a second, bigger ring of {link("moonsteel_gate_frame")} with an arch on the back,
* a {link("gate_lens_housing")} on top of the arch,
* a {link("selenite_block")}, and an {link("aresite_block")} under the centre of the pad.

Press **Preview** on the controller for the next tier's required blocks, grouped by
structural section. **Ghost** shows the current tier, not the next-tier upgrade.

## Reach Galaxy 2

A formed Tier 2 survival gate reaches Cerulon, Galaxy 2's wasteland slots and its
moon slot. Each later galaxy's moon opens at that galaxy's tier too; Tier 6 is not
required for moons. Lower-tier gates cannot reach higher galaxies. Charge and
ownership checks still apply, unlike the unrestricted admin test-hub gates.

In Cerulon's Concord Vault, uncommon chests can hold the
{link("cobaltium_upgrade_smithing_template")},
{link("cyrrium_upgrade_smithing_template")} and
{link("aurelion_upgrade_smithing_template")}. This provides a first-template source
while the Prism Spire is unfinished. A template is not guaranteed in every chest;
the existing duplication recipes let you copy one after finding it.

## Controller upgrades

The controller has upgrade slots (one at Tier 1):

* {link("refracting_lens")}: retained for compatibility; no discount on the fixed gate-jump tariff.
* {link("cryo_core")}: the gate charges twice as fast.
* {link("capacity_coil")}: 2 more passengers fit on the pad.

## Jump budget and standing plans

Player gate jumps cost exactly **100,000 / 200,000 / 400,000 / 800,000 /
1,600,000 / 3,200,000 FE** at tiers 1–6. A successful group jump pays once;
passenger count, same-galaxy travel and lenses do not change this tariff.
Cancelled or invalid launches do not charge. Admin showcase gates remain free.

Open the controller and choose **Plans**, then **Tier 1–6** to show a standing
wireframe anchored to that controller. Green means correct, cyan missing and red
wrong block. A selected plan does not upgrade or construct the actual gate.
The hologram above the terminal shows the selected galaxy/planet and charging
countdown. Dimension jumps use the galaxy-to-planet transition artwork.
""")
print(sorted(os.listdir(G)))
