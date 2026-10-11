---
navigation:
  title: 19. Gas Separation
  icon: zerog_tweaks:water_separator
  position: 190
  parent: index.md
item_ids:
  - zerog_tweaks:water_separator
  - zerog_tweaks:gas_canister
---

# Water Separation and Gas Transport

<Row>
  <BlockImage id="zerog_tweaks:water_separator" scale="3" />
  <ItemImage id="zerog_tweaks:gas_canister" scale="3" />
</Row>

1. Place the Water Separator. Open its panel to identify the six **world faces**.
2. The default **Up** face accepts water; **East** supplies hydrogen and **West** supplies oxygen.
3. Connect power to an enabled FE input face. All six FE faces start enabled.
4. Use **gas tubes**, not liquid pipes, to collect the gases in separate tanks.
5. A gas canister holds up to 1,000 mB of one gas; partially filled canisters can be topped up with that same gas.

Default processing uses 10 mB water and 2,000 FE over 100 ticks, producing
20 mB hydrogen and 10 mB oxygen. Server settings can change these amounts;
the live Recipe panel shows the current values. Three tanks hold 16,000 mB each
and the FE buffer holds 200,000 FE. Either full gas tank safely pauses the job.
Inputs are consumed only when a whole cycle completes.

## Tubes and cards

Gas-tube tiers follow Copper, Nullifite, Cyrrium, Tectium, Wraithsteel and Astrium.
Keep hydrogen and oxygen networks separate. The weakest connected tier limits
shared transfer rates; higher-tier branches do not bypass lower-tier sections.
The separator accepts Acceleration and Energy Coil cards tiers 1-6, with the
existing bounded speed/energy effects. It does not support Compact or Void cards.

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
