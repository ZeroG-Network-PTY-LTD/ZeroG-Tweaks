---
navigation:
  title: "Tier 2 / Moonsteel"
  icon: zerog_tweaks:moonsteel_gate_frame
  position: 20
  parent: 16_gate_atlas.md
---

# Tier 2 / Moonsteel

Footprint 7 × 7; complete target layout, not an additive shopping list. Jump: 200,000 FE. Earlier columns must grow to the target height.

| Block | Required |
| --- | ---: |
| <ItemLink id="zerog_tweaks:aresite_block" /> | 1 |
| <ItemLink id="zerog_tweaks:gate_controller" /> | 1 |
| <ItemLink id="zerog_tweaks:gate_energy_port" /> | 1 |
| <ItemLink id="zerog_tweaks:gate_lens_housing" /> | 1 |
| <ItemLink id="zerog_tweaks:gate_pad_plate" /> | 9 |
| <ItemLink id="zerog_tweaks:gate_pylon" /> | 16 |
| <ItemLink id="zerog_tweaks:moonsteel_gate_frame" /> | 35 |
| <ItemLink id="zerog_tweaks:nullifite_gate_frame" /> | 16 |
| <ItemLink id="zerog_tweaks:selenite_block" /> | 1 |

## Step 1 / Layer y=-2 — Buried core

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:aresite_block" x="3" y="0" z="3" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 2 / Layer y=-1 — Foundation rings

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="0" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="1" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="2" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="3" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="4" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="1" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="2" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="2" y="1" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="3" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="3" y="1" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="4" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="4" y="1" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="1" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="0" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="1" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="2" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="3" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="4" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 3 / Layer y=+0 — Pad and column feet

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_pylon" x="1" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="2" z="5" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pad_plate" x="4" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="4" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="4" y="2" z="4" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="2" z="5" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 4 / Layer y=+1 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_pylon" x="1" y="3" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="3" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="3" z="6" />
  <Block id="zerog_tweaks:gate_controller" x="3" y="3" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="3" z="1" />
  <Block id="zerog_tweaks:gate_energy_port" x="5" y="3" z="3" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="3" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="3" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 5 / Layer y=+2 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_pylon" x="1" y="4" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="4" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="4" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="4" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="4" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="4" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 6 / Layer y=+3 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_pylon" x="1" y="5" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="5" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="5" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="5" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="5" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="5" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 7 / Layer y=+4 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="6" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="2" y="6" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="3" y="6" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="4" y="6" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="6" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 8 / Layer y=+5 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:gate_lens_housing" x="3" y="7" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Step 9 / Layer y=+6 — Services / columns / rear arch

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:selenite_block" x="3" y="8" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

## Final check

<GameScene zoom="1.6" interactive={true}>
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="0" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="1" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="2" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="3" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="4" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="0" y="1" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="1" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="1" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="2" z="5" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="3" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="3" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="3" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="4" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="4" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="4" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="5" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="1" y="5" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="5" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="1" y="6" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="2" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="2" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="2" y="1" z="6" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="2" y="2" z="4" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="2" y="6" z="6" />
  <Block id="zerog_tweaks:aresite_block" x="3" y="0" z="3" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="3" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="3" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="3" y="1" z="6" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="3" y="2" z="4" />
  <Block id="zerog_tweaks:gate_controller" x="3" y="3" z="1" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="3" y="6" z="6" />
  <Block id="zerog_tweaks:gate_lens_housing" x="3" y="7" z="6" />
  <Block id="zerog_tweaks:selenite_block" x="3" y="8" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="4" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="4" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="4" y="1" z="6" />
  <Block id="zerog_tweaks:gate_pad_plate" x="4" y="2" z="2" />
  <Block id="zerog_tweaks:gate_pad_plate" x="4" y="2" z="3" />
  <Block id="zerog_tweaks:gate_pad_plate" x="4" y="2" z="4" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="4" y="6" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="1" z="0" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="1" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="2" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="3" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="4" />
  <Block id="zerog_tweaks:nullifite_gate_frame" x="5" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="1" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="2" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="2" z="5" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="3" z="1" />
  <Block id="zerog_tweaks:gate_energy_port" x="5" y="3" z="3" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="3" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="3" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="4" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="4" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="4" z="6" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="5" z="1" />
  <Block id="zerog_tweaks:gate_pylon" x="5" y="5" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="5" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="5" y="6" z="6" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="0" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="1" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="2" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="3" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="4" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="5" />
  <Block id="zerog_tweaks:moonsteel_gate_frame" x="6" y="1" z="6" />
  <IsometricCamera yaw="195" pitch="30" />
</GameScene>

Open the controller and **Align**. Missing parts are grouped by structural section. Connect generation to a Gate Energy Port and verify the shared FE buffer before launch. [Back to the atlas](16_gate_atlas.md).
