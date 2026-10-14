"""Concord Codex GuideME pages (v1): the Sol loop walkthrough.

usage: python write_guide.py <code-branch src/main/resources/assets/zerog_tweaks dir>
Optional --pages-only stages chapter edits without resolving the runtime gate
illustration helper. Full regeneration remains the default for the code checkout.
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

**Tip:** open the controller and choose **Plans**, then **Plan T1** for the standing wireframe for
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

**Auto-build:** place and claim the controller, then use **Plans → Build T1**.
Carry the missing structural blocks in your inventory. The server checks all
materials first, preserves matching blocks and your controller, and refuses
obstructions without consuming supplies. Use **Build T2–T6** to add later tiers.
This is not free construction, even in creative. Clear the required footprint
first; the builder does not excavate or remove other buildings.

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
| Additional passengers | No extra jump fee |

At 50 FE/t one Tier 1 trip needs 100 seconds of burning. The controller screen shows the stored FE.

Next: [launch](04_launch.md).
""")

page("04_launch.md", "4. Launch", "zerog_tweaks:gate_pad_plate", 40, body=f"""
# 4. Launch

A formed gate with stored FE lights its pillars with short beacon-style lamps.
During warm-up the pillars activate in sequence; beams grow taller and pulse as
the rift and lift approach. These are visual indicators, not beacon buffs.

1. **Right-click the Gate Controller.** The first player to do this owns the gate. Only the owner can launch it.
2. Pick a destination: **moon** or **mars** at Tier 1. Use the arrow buttons to page through the list.
3. Stand on the pad and press **Engage**. A Tier 1 pad carries **2 players**.
4. The initiator is already Ready; other passengers open the controller and press **Ready** before the 5-second countdown ends.
   Step off the pad or press **Cancel** to abort.

Tamed pets owned by a passenger, and mobs on a passenger's lead, come along.
Remain above the pad during the launch lift; stepping sideways out of the pad
cancels. A refused engagement or cancelled launch reports its reason. Successful
travel uses the ZeroG galaxy/planet transition; a refused launch is not a teleport.

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

Hover a ZeroG block in inventory to see its loaded mining requirement. Trying to mine it with a weaker tool
shows a red requirement above the hotbar. Moonsteel needs **Ferrox**, not Nullifite: visit Mars for Ferrox first.
Stone variants use their own tool tags; they do not automatically inherit the ore ladder.

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
structural section. **Plans** offers both standing previews and inventory-funded
construction for every tier.

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

Open the controller and choose **Plans**, then **Plan T1–T6** to show a standing
wireframe anchored to that controller. Green means correct, cyan missing and red
wrong block. A selected plan does not upgrade or construct the actual gate.
The separate **Build T1–T6** controls check and consume the missing blocks.
The hologram above the terminal shows the selected galaxy/planet and charging
countdown. Dimension jumps use the galaxy-to-planet transition artwork.
""")
page("10_planet_exploration.md", "10. Planetary Exploration", "zerog_tweaks:charwood_planks", 100, body="""
# 10. Planetary Exploration

## Rare settlements

Look on solid, gently sloping land. Settlements use local doors, wet farmland and
native ground edges, not suspended sea platforms. Villages are rare: each
50-by-50-chunk region has one possible site, and unsuitable terrain rejects it.
Every Rustborn settlement keeps its hand-cut Aresite core shrine.

## Abandoned mines

Underground passages branch from a main corridor. Follow timber supports and
occasional rails to explore; a chest may hold the existing expedition rewards.
Moon and Eidolon use Hoarwood, Mars and Skarn Charwood, Cerulon Shardwood and
Solvane Gildwood. Surrounding ores still need the correct mining-tier tool.
Mines are not guaranteed in a short search and do not replace boss chambers.

## Living caves

Watch for planet-coloured mushrooms, dripstone, hanging berries and wall vines.
Aquatic cave kelp grows in source-water pockets, not flowing streams. Existing
Prismlings inhabit Cerulon's dark crystal caves, including covered caves above
sea level. Being underground does not make every surface creature a cave mob.

## Collapsed Forges

Search dry Skarn terrain and volcanic wasteland ash or basalt fields for ruined
Concord smithies. Scorched Marble supports and broken Charwood roof beams frame
an open passage, cold furnace and anvil. The chest can hold Ruskite, Pyrium,
Tectium and Skarnite upgrade templates plus existing forge salvage; no individual
chest guarantees a template. This ruin does not implement the Rift Tyrant fight
or new smith dialogue.

## Small Hollow Fleet wrecks

On Eidolon, search dry Frozen Graveyard terrain for damaged ships made from
Hull Plating and Corroded Hull. Enter through the broken sides; the central
corridor leads to a real loot chest. Existing Derelict Wreck loot can include
Salvium, Wraithsteel, Palladine and Eidolite upgrade templates, but individual
chests do not guarantee one. Cryo Pods and Broken Consoles are existing salvage
blocks here, not a completed final-log encounter. Large wrecks, their guardian
and the Captain's peaceful route remain separate unfinished content.

## Solar Shrines

On Solvane, search dry Corona Flats, Sunspot Plateaus and Gildwood Oasis terrain
for open circular courts of Solar Stone, Radiant Bricks and Gildwood, with lit
pillars. Follow the central approach to the chest. Existing rewards can include
Photium, Radiantine, Astrium and Solvanite upgrade templates; no individual chest
guarantees one. Shrine hymns, the Dying Star encounter and the Heart of Solvane
ending remain unfinished. Finding a shrine does not complete those story tasks.

These changes appear in newly generated terrain; explored chunks keep their
existing blocks. Read [the mining ladder](07_mining.md) before harvesting ores.
""")
page("11_genetics.md", "11. Genetics Recipes", "zerog_tweaks:concord_codex", 110, body="""
# Genetics Recipes

The orbital addon supplies the Geno Station and Genetic Splicer. Their **Recipes**
button opens three read-only tabs: Items, Recipes and Upgrades. Hover shortened
lines for the full text and scroll for all details. The Geno Station recipe page
switches between Analyse and Sample using its bottom button. Browsing does not
start a job or move items; use the machine's normal operation buttons to work.

## Analysis and sampling

Insert one filled Productive Bees cage with five saved valid traits. Analysis
returns an analysed cage without changing its traits. Sampling requires that
analysed specimen, one serum vial and a selected gene; it returns the cage and
one serum carrying that gene's value.

Each job consumes either one Honey Drop, one Honey Bottle, or 250 mB of supported
honey from the tank. A valid item catalyst takes priority over the tank. Analysis
returns an empty Honey Bottle container to output slot 4; sampling returns it to
a free recovery slot 5-15 because slot 4 contains the serum. Fluid and Honey Drop
routes return no bottle.

## Splicing

Use an analysed specimen and one valid serum. Royal Jelly gives 75% success;
Cosmic Jelly gives 100%. Each may be supplied as one item or 250 mB from the tank.
The serum and catalyst are consumed on either outcome. Success returns a cage
with only that gene changed; failure returns the original cage. Both outcomes
return one empty serum vial. Leave room for both outputs before starting.

## Power and cards

Base powered analysis is 100 ticks / 2,000 FE, sampling 300 ticks / 6,000 FE, and
splicing 400 ticks / 24,000 FE. The Geno Station works four times slower without
power; the Splicer requires power. Mixed-power jobs vary with powered work.

Acceleration and Energy Coil cards have separate sockets and tiers 1-6, capped
at 2.5x speed and 30% total FE savings. The pages use server-synced current effects.
Cards do not improve splice chance or traits. Compact and Void are unsupported.
Exact crafting costs and advanced Codex research rules remain pending.
""")
page("12_generators.md", "12. Generator Recipes", "zerog_tweaks:combustion_generator", 120, body="""
# Generator Recipes

Combustion Generator, Solar Array and Fusion Reactor have read-only Items,
Recipes and Upgrades tabs. Select a fuel in Items, then scroll or hover shortened
recipe lines for full details. Browsing never starts a job or moves items.

## Combustion

Wood items, coal forms and supported planetary fuels burn; dusts are rejected.
One fuel item is consumed on ignition. The page shows its actual active burn
ticks, production rate and fresh-burn FE budget. Saved fractional carry may add
one FE across burns. A full buffer pauses burning rather than wasting paid fuel.

## Fusion

Only Fusion Dust is accepted. Its duration and base output come from the server
configuration. The page describes a future burn using that configuration;
already ignited fuel retains its saved base rate. There is no gas or liquid fuel
route, catalyst or item byproduct.

## Solar

There is no fuel slot. Generation requires daytime, skylight and visible sky.
An opaque roof or thunder stops generation; rain reduces it. Moon, Eidolon and
Solvane have configured multipliers. The current environment rate is displayed;
free buffer space limits the actual FE generated.

## Modules and routing

All three generators accept up to three Flux Modules, each adding 25% production
rate and one base buffer capacity. Modules do not shorten fuel duration.
Acceleration, Energy Coil, Compact and Void cards are unsupported here.
Solar/Fusion module removal is blocked if the smaller buffer would lose stored FE.

Power faces are Output or Off, never FE input. Automatic push is shared across
enabled faces: Combustion uses 1,000 FE/t, Solar/Fusion use the server transfer
setting. Production rate is not a cable transfer guarantee. Exact survival
crafting costs and client layout approval remain separate.
""")
page("13_alveary_recipes.md", "13. Alveary Recipes", "zerog_tweaks:concord_codex", 130, body="""
# Alveary Production Recipes

Open the controller's Recipes button for Items, Recipes and Upgrades. Hover
shortened lines and scroll for all details. Items lists accepted frames; the bee
still goes in the main input slot. Browsing is read-only: it cannot start a job,
autofill inventory, sort outputs or toggle void.

## Bee inputs and products

Use one supported orbital bee or a captured Productive Bees specimen with five
saved valid traits. Production retains the specimen. Orbital species produce
their registered comb; Productive Bees outputs are resolved from the server's
loaded advanced-beehive recipes, including item components, quantity ranges and
chances. Saved bee productivity is included in the displayed ranges.

The recipe snapshot updates about once per second while the controller menu is
valid. Removing or changing the specimen updates its products. More than 32
product entries are explicitly marked truncated rather than silently hidden.

## Frames and cycle time

Existing controller tiers 1-7 unlock 3, 4, 6, 8, 12, 18 and 27 frame slots.
Honeyed, Starlit and Starmetal frames each add 15% cycle-speed productivity;
Proven and Impregnated add 10%; Restraint and Oblivion subtract 5%; other
supported frames add 5%. The total multiplier is bounded from x0.25 to x4.
Frames shorten or lengthen the cycle; they do not multiply output quantities.

The page shows the current runtime cycle. Tier 3 and above consume 20 times the
tier in FE per active tick; tiers 1-2 require no FE. The displayed full-cycle
budget assumes unchanged frames and catalyst availability throughout the job.
Day/night behavior, rain tolerance, formation, blocked products or honey storage
may pause progress; paused ticks do not represent productive work.

## Honey and optional Starlight

Tier 3 and above produce 250 mB of local Sol-planet honey alongside products on
every completed cycle. Other dimensions use Moon Honey. The honey tank holds
8,000 mB and cannot mix honey types. Use the honey/output service port to drain it.

Tier 6 and above have a 4,000 mB Liquid Starlight catalyst tank. At least 25 mB
gives x1.2 cycle speed; 25 mB is consumed when the cycle completes. This boost is
optional. Service ports handle power, item and fluid automation; the controller
is the interaction terminal, not a cable shortcut.

## Existing limits

Acceleration, Energy Coil, Compact and Void cards are unsupported here. Existing
eject and void buttons remain independent controls, not card upgrades. Native
lifespan/territory alleles, additional climate/module rules and the Codex research
milestone map remain pending specifications. This chapter does not introduce
seven-wide layouts or survival crafting costs.
""")
page('14_frame_recipes.md', '14. Frame Recipes', 'zerog_tweaks:concord_codex', 140, body='''
# Frame Production Recipes

Open Items, Recipes and Upgrades on the Frame Assembler, Frame Component
Assembler or either Infusion Altar. Clicking an ingredient or output lists
its exact combinations. Both inputs are consumed, one each; output is certain.

## Assembly

Put an Untreated Frame in slot 0 and one material in slot 1:

- Honeycomb makes an Impregnated Frame.
- Starmetal Ingot makes a Starmetal Frame.
- Woven Silk makes an Aero Silk Frame.

## Infusion

Put an Impregnated Frame in slot 0 and one reagent in slot 1:

- Amethyst Shard makes a Proven Frame.
- Cosmic Jelly item makes a Cosmic Vigor Frame.
- Stardust makes a Starlit Frame.

The result uses slot 2, except Frame Infusion Altar, which uses slot 3.
Its old slot 2 is recovery-only. A blocked output pauses processing without
consuming ingredients. Completion takes 201 processing ticks in the current
runtime. These machines now require cable power: the default is 20 FE per work
tick, or 4,020 FE per base job. Their six faces have independent power/input
controls, and Acceleration/Energy Coil cards use the existing 2.5x/30% caps.

## Silk and centrifuges

Silk Weaver consumes one Silk Thread and produces one Woven Silk in slot 3.
Slots 1 and 2 remain recovery-only, not pattern or catalyst inputs. Its base job
is 200 ticks and 4,000 FE by default. Gravitational Centrifuge shares the normal
Centrifuge's comb recipes and default 20 FE per work tick. Unpowered or blocked
jobs consume no ingredients or processing FE.

The Recipes button opens a separate read-only view within the current menu, so
Items, Recipes and Upgrades remain usable without squeezing inventory or side
controls. Back or Escape returns to the machine; browsing never moves items.

Browsing does not autofill or start jobs. Survival crafting costs remain deferred;
these are the existing processing combinations, not new crafting recipes.
''')
page('15_stardust_smelter.md', '15. Stardust Smelter', 'zerog_tweaks:concord_codex', 150, body='''
# Stardust Smelting

Put a supported comb in slot 0 and furnace fuel in slot 1. Slot 2 holds dust.
Open Recipes, then click a comb, dust or fuel in Items to inspect the combinations.

- One Meteor Comb produces two Stardust.
- One Nebula Comb produces three Stardust.
- One Molten Comb produces one Stardust.

Each job takes 201 hot ticks. Fuel uses Minecraft's smelting burn duration,
not one fuel item per comb. One coal supplies 1,600 hot ticks: seven consecutive
jobs with 193 ticks left for the next job. Coal blocks last 16,000 ticks.
The Items tab shows each accepted fuel; selecting one displays its actual budget.

Fuel is consumed when the fire starts. Container fuels return their container.
A cold blocked machine does not ignite fuel; an already lit fire continues to
burn while idle or blocked, like a furnace. Inputs are consumed only on successful
completion. Running out of heat resets incomplete work without consuming the comb.
Remaining fire and progress survive save/reload. Changing comb type resets work.

No FE or upgrade cards are required or supported here. This repair does not set
survival crafting costs, change combustion-generator fuels or alter comb yields.
''')
page('19_gas_separation.md', '19. Gas Separation', 'zerog_tweaks:water_separator', 190,
     items=['zerog_tweaks:water_separator', 'zerog_tweaks:gas_canister'], body='''
# Water Separation and Gas Transport

<Row>
  <BlockImage id="zerog_tweaks:water_separator" scale="3" />
  <ItemImage id="zerog_tweaks:gas_canister" scale="3" />
</Row>

1. Find the Water Separator in Functional Blocks. Place its front toward you;
   horizontal placement and rotation are supported. Open its panel to identify
   the six **world faces**. Rotating the front does not remap configured ports.
2. The default **Up** face accepts water; **East** supplies hydrogen and **West** supplies oxygen.
3. Connect power to an enabled **non-front** FE input face. Stored face settings
   start enabled, but the front terminal always rejects external power and pipes.
4. Use **gas tubes**, not liquid pipes, to collect the gases in separate tanks.
5. A gas canister holds up to 1,000 mB of one gas; partially filled canisters can be topped up with that same gas.

Default processing uses 10 mB water and 2,000 FE over 100 ticks, producing
20 mB hydrogen and 10 mB oxygen. Server settings can change these amounts;
the live Recipe panel shows the current values. Three tanks hold 16,000 mB each
and the FE buffer holds 200,000 FE. Either full gas tank safely pauses the job.
Inputs are consumed only when a whole cycle completes.

## Gas catalogue and storage

Creative testing uses the **ZeroG: Gases** tab: one empty canister, filled Oxygen
and Hydrogen canisters, and both gases in every existing storage-tank tier.
Prefilled entries are test supplies, not new survival crafting recipes.

<Row>
  <BlockImage id="zerog_tweaks:copper_fluid_tank" scale="2" />
  <BlockImage id="zerog_tweaks:astrium_fluid_tank" scale="2" />
</Row>

Tank capacities are Copper 5,000; Nullifite 20,000; Cyrrium 100,000;
Tectium 500,000; Wraithsteel 2,000,000; Astrium 5,000,000 mB.
Hover filled tanks to read the gas and exact amount. Place one, then right-click
to inspect its **Gas Storage Tank** panel and world-face controls. Breaking or
wrench-picking-up a filled shell preserves its contents when placed again.

Use a separate tank/network for each gas; water, Oxygen and Hydrogen cannot mix
in one tank. The same shell supports liquid storage too. Its fullness display
is not a real-world pressure gauge. Survival supplies come from the separator
and gas canisters/tubes, not free creative-tab contents.

## Tubes and cards

Gas-tube tiers follow Copper, Nullifite, Cyrrium, Tectium, Wraithsteel and Astrium.
Keep hydrogen and oxygen networks separate. The weakest connected tier limits
shared transfer rates; higher-tier branches do not bypass lower-tier sections.
The separator accepts Acceleration and Energy Coil cards tiers 1-6, with the
existing bounded speed/energy effects. It does not support Compact or Void cards.
The front terminal is closed to pipes, cables and automated items. Other faces
support configurable water/gas roles and power; item automation accepts supported
upgrade cards only, not arbitrary processing ingredients. Rotation preserves
saved world-face roles but always closes whichever face is now the terminal.

## Incorrect connections

An enabled liquid pipe directly attached to a gas output vents up to 10 mB per
second by default; the server can adjust or disable this loss. Hydrogen clouds
give survival players within two blocks brief nausea and weakness when the
outlet is unobstructed. Moving away stops refresh and the effects expire.
Oxygen vent particles are non-toxic. Correct gas tubes, disabled faces, open
outlets and full tanks do not leak. There are no explosions or terrain damage.
Pressure gauges mean tank fullness, not a real physical pressure unit.

Exact survival crafting costs and dedicated separator artwork remain pending.

## Recipes and diagnostics

The Recipes button opens a read-only view inside the current machine menu.
Back or Escape returns to the machine without closing its inventory. The
separator's recipe, container examples and upgrade tabs show server-configured
mB, FE and processing time. Bucket and canister icons are examples, not a
requirement to consume a whole container.

In Configure mode, right-click a supported machine with the Flux Wrench for
a temporary, read-only port hologram. It shows six world faces and the stored
energy snapshot for 15 seconds; click again to refresh. It does not alter modes.
''')
page('20_wasteland_creatures.md', '20. Wasteland Wildlife', 'zerog_tweaks:rime_stalker_spawn_egg', 200,
     items=['zerog_tweaks:rime_stalker_spawn_egg', 'zerog_tweaks:crater_drifter_spawn_egg', 'zerog_tweaks:ash_strider_spawn_egg'], body='''
# Wasteland Wildlife

<Row>
  <ItemImage id="zerog_tweaks:rime_stalker_spawn_egg" scale="3" />
  <ItemImage id="zerog_tweaks:crater_drifter_spawn_egg" scale="3" />
  <ItemImage id="zerog_tweaks:ash_strider_spawn_egg" scale="3" />
</Row>

## Rime Stalker

Frozen wasteland glaciers, ice-spike forests and frozen canyons host this
predator. It approaches from behind when you face it at a distance, then bites
at close range. A successful bite adds 100 frozen ticks; the stalker itself
cannot freeze. Existing loot includes Frost Pelt and a rare Cryo Core.
Custom snowstorm concealment is pending while custom weather is paused.

## Crater Drifter

Barren cratered plains, dust badlands and canyon scars host this neutral
floating scavenger. It drifts above the surface and does not seek out peaceful
players. Attacking one provokes retaliation and alerts nearby drifters.
It drops one Meteorite Fragment every 6,000 ticks; the timer survives reload.
Its existing death loot includes Stardust. This is not a boss or a source of
Broken Consoles, Dormant Wisps or Codex books.

## Ash Strider

Volcanic basalt fields, ash plains and lava lakes host this neutral mount.
It can stand on lava and is immune to fire. Feed Cinder Caps to breed;
use a saddle to mount, and the vanilla Warped Fungus on a Stick to steer.
Breeding produces another Ash Strider, never a vanilla Strider.
It retaliates when hurt but does not hunt players. Its existing rare death
loot is Heatproof Plating. A dedicated Cinder-Cap steering tool and revised
stomp artwork remain future work; no Nether jockeys spawn with it.

## Bog Lurker

Toxic acid swamps, mud flats and moss bogs host this hostile amphibian.
It is immune to acid and poison, moves faster through acid and rests with its
eyes near the surface. Its spit is a moving projectile: 5 damage and Poison II
for 80 ticks on a successful hit, within 10 blocks and with line of sight.
It does not corrode terrain. Existing drops include Lurker Legs, Venom Glands
and a rare Neutralizer. Dedicated swim/spit artwork and natural density need review.

Idle lurkers seek nearby loaded acid pools. Acid immersion permits spawning
only when unobstructed; natural acid-pool spawning requires dim light.
Acid and poison immunity also protects them while chasing prey in a pool.

## Ocean Tidewraith

Regular Tidewraiths can spawn above exposed water in deep trenches, kelp jungles
and island chains. They are aggressive flying aquatic predators, travelling in
packs of 3-4 and pursuing prey at higher elevations. Non-magma liquid immersion
does not drown, poison, freeze or burn them; lava and magma slag remain dangerous.
Defaults use a one-in-eight pack-start check and a nearby limit of four
within 128 blocks. Server settings
can change the chance and limit. Covered water, dry land and acid are rejected.
This does not add natural boss spawning or require player insomnia.

Spawn eggs now create these mobs. Server registration and habitat checks do
not establish natural encounter density or client visual approval.
''')
page("21_industrial_compressor.md", "Industrial Compressor", "zerog_tweaks:industrial_compressor", 21, '''
# Industrial Compressor

The press shapes recovered planetary metals into manufacturing components.
This is a powered processor, not a fluid refinery.

1. Place the machine with its terminal facing you.
2. Connect power to a side, back, top or bottom face. **The front is not a port.**
3. Put a **Plate Press** in the tooling slot and **2 ingots** in the input.
   A completed job makes **1 compressed plate**, using **2,000 FE / 100 ticks**.
4. Swap to a **Cog Press** and insert **4 ingots**. This makes **1 cog**,
   using **4,000 FE / 160 ticks**. The press is reusable and is not consumed.
5. Use **Recipes** to inspect every loaded material combination and current
   upgrade-adjusted energy/time. Full outputs or missing power pause safely.

All21 planetary manufacturing metals plus vanilla Copper are supported (44 recipes).
Copper ingots are vanilla items; Copper plates/cogs are ZeroG components. Other materials
are accepted only when an actual pressing recipe exists. Keep one material in
the input slot. Tooling is separate from Acceleration/Energy Coil/Compact/Void cards.

Side controls select reagent, tooling/catalyst or output access independently of
power. The front always stays closed to automation, even after rotation.
There is no fluid recipe or decorative fluid port. Exact survival crafting costs
for the machine and presses remain pending approval; creative testing is available.

<ItemImage id="zerog_tweaks:industrial_compressor" scale="3" />
<ItemImage id="zerog_tweaks:plate_press" scale="2" />
<ItemImage id="zerog_tweaks:cog_press" scale="2" />
''')
print(sorted(os.listdir(G)))
if '--pages-only' not in sys.argv[2:]:
    from illustrated_journal import enhance
    enhance(A)
