---
navigation:
  title: 2. Build the T1 Gate
  icon: zerog_tweaks:gate_controller
  position: 20
  parent: index.md
item_ids:
  - zerog_tweaks:gate_controller
  - zerog_tweaks:nullifite_gate_frame
  - zerog_tweaks:gate_pad_plate
  - zerog_tweaks:gate_pylon
  - zerog_tweaks:gate_energy_port
---

# 2. Build the T1 Gate

The gate is a multiblock. This is the whole Tier 1 build. Drag to rotate, scroll to zoom.

<GameScene zoom="4" interactive={true}>
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="0" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="0" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="0" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="0" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="0" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="0" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="0" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="0" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="0" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="0" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="0" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="0" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="0" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="0" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="0" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="0" z="4" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="1" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="1" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="1" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="1" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="1" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="1" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="1" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="1" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="1" z="3" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="1" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="2" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="3" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="1" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="3" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="1" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="2" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="3" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="1" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="3" z="4" />
  <Block id="zerog_tweaks:gate_energy_port" x="4" y="2" z="2" />
  <Block id="zerog_tweaks:gate_controller" x="2" y="2" z="0" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Parts list

| Part | Count | Where it goes |
| --- | --- | --- |
| <ItemLink id="zerog_tweaks:nullifite_gate_frame" /> | 16 | A 5x5 ring, one layer **below** the pad |
| <ItemLink id="zerog_tweaks:gate_pad_plate" /> | 9 | The 3x3 pad in the middle of the ring |
| <ItemLink id="zerog_tweaks:gate_pylon" /> | 12 | Four corner columns, 3 tall, on the ring's corners |
| <ItemLink id="zerog_tweaks:gate_controller" /> | 1 | Any legal service position, one block above the pad |
| <ItemLink id="zerog_tweaks:gate_energy_port" /> | 1 | Another legal service position on any horizontal side |

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
