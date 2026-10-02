# Upgrade smithing templates (v1.3)

Every set after Nullifite is made at the smithing table, the same way netherite is made from diamond:
**template + the previous set's piece + the new set's ingot or gem**. Enchantments and trims carry over.
Nullifite is crafted from ingots, like diamond. The chain follows the mining ladder.
The precious sets (Aurelion, Pyrium, Palladine, Radiantine) branch off their world's entry set.

| Set | Smithing table | Template found in | Copy recipe (gives 2): ring x7 + middle |
| --- | --- | --- | --- |
| Ferrox | Nullifite piece + Ferrox Ingot | Mars Crash Site (Mars) | 7 Nullifite Ingot + Martian Stone |
| Moonsteel | Ferrox piece + Moonsteel Ingot | Mars Crash Site (Mars) | 7 Ferrox Ingot + Martian Stone |
| Olympium | Moonsteel piece + Olympium Ingot | Mars Crash Site (Mars) | 7 Moonsteel Ingot + Martian Stone | existing id
| Cobaltium | Olympium piece + Cobaltium Ingot | Prism Spire (crystal wasteland, Galaxy 2) | 7 Olympium Ingot + Prismstone |
| Aurelion | Olympium piece + Aurelion Ingot | Prism Spire (crystal wasteland, Galaxy 2) | 7 Olympium Ingot + Prismstone |
| Cyrrium | Cobaltium piece + Cyrrium Ingot | Prism Spire (crystal wasteland, Galaxy 2) | 7 Cobaltium Ingot + Prismstone |
| Cerulite | Cyrrium piece + Cerulite | Prism Spire (crystal wasteland, Galaxy 2) | 7 Cyrrium Ingot + Prismstone | existing id
| Ruskite | Cerulite piece + Ruskite Ingot | Collapsed Forge (volcanic wasteland, Galaxy 3) | 7 Cerulite + Scoria |
| Pyrium | Cerulite piece + Pyrium Ingot | Collapsed Forge (volcanic wasteland, Galaxy 3) | 7 Cerulite + Scoria |
| Tectium | Ruskite piece + Tectium Ingot | Collapsed Forge (volcanic wasteland, Galaxy 3) | 7 Ruskite Ingot + Scoria |
| Skarnite | Tectium piece + Skarnite | Collapsed Forge (volcanic wasteland, Galaxy 3) | 7 Tectium Ingot + Scoria | existing id
| Salvium | Skarnite piece + Salvium Ingot | Derelict Wreck (Eidolon) | 7 Skarnite + Permafrost |
| Palladine | Skarnite piece + Palladine Ingot | Derelict Wreck (Eidolon) | 7 Skarnite + Permafrost |
| Wraithsteel | Salvium piece + Wraithsteel Ingot | Derelict Wreck (Eidolon) | 7 Salvium Ingot + Permafrost |
| Eidolite | Wraithsteel piece + Eidolite | Derelict Wreck (Eidolon) | 7 Wraithsteel Ingot + Permafrost | existing id
| Photium | Eidolite piece + Photium Ingot | Solar Shrine (Solvane) | 7 Eidolite + Solar Stone |
| Radiantine | Eidolite piece + Radiantine Ingot | Solar Shrine (Solvane) | 7 Eidolite + Solar Stone |
| Astrium | Photium piece + Astrium Ingot | Solar Shrine (Solvane) | 7 Photium Ingot + Solar Stone |
| Solvanite | Astrium piece + Solvanite | Solar Shrine (Solvane) | 7 Astrium Ingot + Solar Stone | existing id

The copy recipe follows vanilla: 7 of the base set's material (as diamonds are to netherite), the template, and the stone of the place it's found.
Bosses still drop their tier's main template (Prism Sentinel: Cerulite, Rift Tyrant: Skarnite, and so on).

## Install (goes on `1.21.x`)
1. **Java:** copy `java/registry/ZGUpgradeTemplates.java` into `src/main/java/net/zerog/tweaks/registry/`.
   - In `ItemInit`, delete the five `registerSimpleItem("<set>_upgrade_smithing_template")` lines (`OLYMPIUM_`, `CERULITE_`, `SKARNITE_`, `EIDOLITE_`, `SOLVANITE_UPGRADE_SMITHING_TEMPLATE`).
   - Call `ZGUpgradeTemplates.init();` in `ItemInit.register()` next to `ZGTrims.init()`.
   - The ids don't change; the templates just become real `SmithingTemplateItem`s with the netherite-style tooltip and empty-slot icons.
2. **Data:** copy `data/` onto `src/main/resources/data/`, overwriting the existing files: 171 smithing recipes, 19 copy recipes, and 5 chest loot tables.
3. **Old recipes:** delete the crafting-table recipes listed in `recipes_to_delete.txt` (126 files). Those sets can now only be made by upgrading, like netherite.
4. **Assets:** copy `assets/` onto `src/main/resources/assets/` (14 new template icons and models). Merge `lang/en_us.additions.json` into `en_us.json`.
5. Re-run `generators/creative_tabs.py` so the new templates sit next to the old ones in the Ingredients tab.
6. Run `./gradlew build` and `runClient`. In the smithing table, check that a Ferrox piece + Moonsteel Ingot + Moonsteel Upgrade gives the Moonsteel piece and keeps its enchantments.
