---
navigation:
  title: "Tier 1 / Nullifite"
  icon: zerog_tweaks:nullifite_gate_frame
  position: 10
  parent: 16_gate_atlas.md
---

# Tier 1 / Nullifite

Footprint 5 × 5; complete target layout, not an additive shopping list. Jump: 100,000 FE. Earlier columns must grow to the target height.

| Block | Required |
| --- | ---: |
| <ItemLink id="zerog_tweaks:gate_controller" /> | 1 |
| <ItemLink id="zerog_tweaks:gate_energy_port" /> | 1 |
| <ItemLink id="zerog_tweaks:gate_pad_plate" /> | 9 |
| <ItemLink id="zerog_tweaks:gate_pylon" /> | 12 |
| <ItemLink id="zerog_tweaks:nullifite_gate_frame" /> | 16 |

## Step 1 / Layer y=-1 — Foundation rings

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="4" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 2 / Layer y=+0 — Pad and column feet

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_pylon" x="0" y="2" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="2" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="2" z="4" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 3 / Layer y=+1 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_pylon" x="0" y="3" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="3" z="4" />
  <Block id="zerog_tweaks:gate_controller" x="2" y="3" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="3" z="0" />
  <Block id="zerog_tweaks:gate_energy_port" x="4" y="3" z="2" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="3" z="4" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 4 / Layer y=+2 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_pylon" x="0" y="4" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="4" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="4" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="4" z="4" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Final check

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="0" y="1" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="2" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="3" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="3" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="4" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="0" y="4" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="4" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="1" y="2" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="4" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="3" />
  <Block id="zerog_tweaks:gate_controller" x="2" y="3" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="4" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="2" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="3" z="0" />
  <Block id="zerog_tweaks:gate_energy_port" x="4" y="3" z="2" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="3" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="4" z="0" />
  <Block id="zerog_tweaks:gate_pylon" x="4" y="4" z="4" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

Open the controller and **Align**. Missing parts are grouped by structural section. Connect generation to a Gate Energy Port and verify the shared FE buffer before launch. [Back to the atlas](16_gate_atlas.md).
