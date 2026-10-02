# Smithing template items (Blockbench)

Blockbench projects (Java Block/Item, texture embedded) for all 29 ZeroG smithing templates:
the 10 armor trim templates and the 19 netherite-style upgrade templates (mining-ladder chain).

| File | What it is |
| --- | --- |
| `<pattern>_armor_trim_smithing_template.bbmodel` | Trim templates: Corona, Crater, Fracture, Geode, Hull, Meteor, Olympus, Prism, Rift, Surge |
| `<set>_upgrade_smithing_template.bbmodel` | Upgrade templates, Ferrox to Solvanite (see `../../zero-g-tweaks-bundle/sheets/gear/upgrade_chain.png`) |
| `templates_preview.png` | All 29 rendered in Blockbench |
| `build_templates.py` | Rebuilds the models from the 16x16 textures on `1.21.x` |

Each model is the item Minecraft builds from the flat sprite: every pixel extruded 1 px thick, with the vanilla
`item/generated` display transforms. In game the templates still use `item/generated` with their 16x16 texture
(`textures/item/<id>.png` on `1.21.x`), so these projects are the editable 3D source, not a replacement model.
