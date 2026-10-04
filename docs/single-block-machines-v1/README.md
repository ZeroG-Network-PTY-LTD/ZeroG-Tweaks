# Single-block genetics machines and machine-interface audit

User change, 2026-10-05: replace the external/assembled Splicer and Geno Station models with one ordinary 16×16×16 block each. Their registry IDs stay unchanged. This supersedes the assembled models in orbital-bees-genetics-v1 for runtime rendering; the original concept work remains archived.

## Artwork and geometry

Both machines have six original native 32×32 faces: hue-shifted dark steel, bevels, brass rails, rivets and recessed cooling vents. The front terminal identifies the machine: violet/cyan DNA for the Splicer, cyan genome bars for the Geno Station. Native 32×128 front strips animate four frames at four ticks each. These animations are decorative—not proof of active genetics or emitted world light. Sides/top/bottom are not texture-stretched front faces.

Block and inventory models share the exact single-cube geometry and texture bindings. All four horizontal facings rotate the terminal correctly. Editable projects in blockbench/ embed six 32×32 first-frame textures. source/ preserves generated models, blockstates, animations metadata, GUI sheets and profile data; generate.py is the authoring source.

![Native face contact sheet, not an in-game capture](single-block-faces.png)

## Live menu coverage

The shipped MachineSlotLayouts table was executed in a Java-only probe, with no Minecraft launch. Eleven non-controller menus get the 256×236 workbench layout: Stardust Smelter, Starmetal Smelter, Silk Weaver, Gravitational Centrifuge, Centrifuge, Frame Assembler, Frame Component Assembler, Frame Infusion Altar, Infusion Altar, Genetic Splicer and Geno Station.

Existing slot numbering, ItemStack handlers, input filters, shift-click rules and 36 player slots are preserved. Input/output arrangements reflect actual counts, including six centrifuge outputs. Empty slots explain their accepted family; purpose panels explain the machine. Server-sent cycle progress is real. No FE/tank values are invented.

**Genetics is still pending.** The installed addon has four Splicer machine slots and two Geno Station slots, not the new five-slot genetics contract. Its existing processing branches are frame infusion and comb smelting placeholders. These menus explicitly show Backend pending and Legacy cycle; no fake Analyse/Sample buttons or genome values are supplied. Trait components, Productive Bees gene access, new server inventories, serum consumption and actual splicing need a separate implementation.

## Other blocks needing interfaces

Six plain ZeroG blocks have no processing block entity: Alloy Forge, Combustion Generator, Solar Array, Fusion Reactor, Salvage Station and Crystal Growth Chamber. Their empty-hand right-click opens a **read-only planned interface**, with numbered slot roles and three use-specific monitoring wells. There are no live inventory slots or fake energy readings.

Twenty registered tier hatches/ports likewise have role-specific read-only plans for items, FE, honey, fluids, pressure or service access. Their empty-hand right-click opens the plan; crouch interactions are left alone. Controller binding/buffer/routing is marked pending.

Already interactive: the nine alveary/apiary/hive menus retain their controller-specific layout; Ore Refinery retains its real processing menu. Gate/arrival controls and their server interactions are not intercepted. Casing, frame housing, structural blocks and decorative plants do not receive invented machine inventories.

## Resource removal and safety

tools/repack_apiary_single_block.py builds a separate resource-only candidate of the user-owned Orbital Bees addon. It replaces both old baked models and their item/blockstate bindings and removes 13 obsolete Splicer/Geno geometry, animation and texture entries. It checks that remaining model texture references resolve, and that every original .class, data/ and META-INF/ payload is byte-identical. Original installed jars are backed up before replacement; source concepts are not deleted. Other addon machines and registry IDs are untouched.

Normal Tweaks assets and the built-in refresh pack ship matching replacements so resource priority cannot restore the old models. The latest art-source layer is explicitly tracked by validators; earlier immutable source hashes are retained.

## Review boundary

Build, slot-table contract, PNG/UV/animation and packaged-byte checks are not GPU tests. Player review is still needed for all facings, first/third-person inventory displays, night visibility, menu clicking/shift-click/resizing and Iris interaction. No saves or worlds are modified by this work.
