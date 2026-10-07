# Item Compact storage — 7 October 2026

Same version: **1.0.12-dev**, Minecraft Java 1.21.1 / NeoForge.

Alloy Forge, Ore Refinery, Crystal Growth Chamber and Salvage Station now accept
one Item Compact card in their middle upgrade socket. The six tiers give each
reagent input a total capacity of **212, 360, 508, 656, 804 or 952 items**.
Catalysts, outputs, player slots and upgrade sockets do not receive this expansion.

Bulk storage is a separate, component-aware reserve, not an oversized ItemStack.
Menus and automation expose ordinary item stacks, refilling from the reserve as
processing or extraction consumes them. Hover over an input to inspect its total
and current capacity. Removing or downgrading a card preserves stored materials;
new deposits are refused while that input exceeds its new capacity. Recover the
materials through the menu or break the machine to receive normal-sized drops.
Different item/component types cannot overwrite an existing reserve.

Cards disable legacy upgrade bonuses consistently with Acceleration and Energy
Coil cards. Legacy cooling items remain recoverable but cannot be newly installed.
No survival costs have been invented: those remain deferred until the owner
reviews the story-aligned workshop progression.

## Tests and delivery

Isolated tests cover six-tier pipe capacity, non-mutating simulations, removal,
save/reload, menu deposits, exact processing consumption, withdrawals and actual
block-removal drops. A withdrawal regression was observed before its repair:
vanilla quick-move mutated the live visible stack and its cleanup could discard a
refilled reserve stack. Withdrawals now move a copy, then extract exactly the
successfully transferred quantity through the storage handler.

The final delivery receipt records the actual test, clean-build, asset-audit and
installation results. Server checks are not client visual approval.

## Still pending

- Void card, saved scrollable output filter, validated controls and selective disposal.
- Dedicated Compact/Void card artwork: reference requested, no replacement invented.
  Compact cards temporarily reuse the existing approved filter-card icon.
- Support for other machine upgrade contracts; these four native processors are
  the scope of this storage implementation.
- Client inspection of input tooltips, menu interactions and layout.
- Other machine recipe/combination adapters and exact survival costs remain deferred.

No player saves or hub terrain are changed by this batch. Prior documentation,
images and released JAR archives are retained.
