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
| <ItemLink id="zerog_tweaks:gate_controller" /> | 1 | Middle of the front edge, one block above the pad |
| <ItemLink id="zerog_tweaks:gate_energy_port" /> | 1 | Middle of a side edge next to the front, one block above the pad |

**Tip:** once the controller is placed, open it and press **Preview**. Every missing block of the
next tier sparkles where it belongs. For an incomplete gate, Preview reports exact missing
block coordinates and the closest matching direction. **Align** turns only your controller
to that direction; it never replaces missing blocks. The Gate Energy Port is required even
if you connect a cable directly to the controller.

## Recipes

The controller is built around the Dormant Wisp from the Courier.

<RecipeFor id="zerog_tweaks:gate_controller" />

<RecipeFor id="zerog_tweaks:nullifite_gate_frame" />

<RecipeFor id="zerog_tweaks:gate_pad_plate" />

<RecipeFor id="zerog_tweaks:gate_pylon" />

<RecipeFor id="zerog_tweaks:gate_energy_port" />

Next: [power it](03_power.md).
