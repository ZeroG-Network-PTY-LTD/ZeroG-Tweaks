# Trim template copy recipes (v1.3)

Each ZeroG trim template is copied like a vanilla one: crafting table, gives 2. Instead of diamonds, the ring is
**7 of the pattern's main item**, and the centre is **the stone of the world where that template is found**.

```
X T X     X = main item (x7)
X S X     T = the trim template
X X X     S = the stone of the world where it is found
```

| Pattern | Template found in | World | Ring (x7) | Centre stone |
| --- | --- | --- | --- | --- |
| Fracture | Buried Observatory | Desert wasteland | 7 Nullifite Ingot | Sunbaked Stone |
| Crater | Impact Site | Barren wasteland | 7 Moonsteel Ingot | Craterstone |
| Olympus | Mars Crash Site | Mars | 7 Olympium Ingot | Martian Stone |
| Geode | Prism Spire | Crystal wasteland | 7 Cerulite | Prismstone |
| Rift | Collapsed Forge | Volcanic wasteland | 7 Rift Opal | Scoria |
| Hull | Derelict Wreck | Eidolon | 7 Salvium Ingot | Permafrost |
| Corona | Solar Shrine | Solvane | 7 Coronite | Solar Stone |
| Surge | Sunken Relay | Ocean wasteland | 7 Brine Crystal | Abyssal Stone |
| Prism | Prism Spire | Crystal wasteland | 7 Prism Cluster | Prismstone |
| Meteor | Impact Site | Barren wasteland | 7 Meteorite Fragment | Craterstone |

## Install (goes on `1.21.x`)
Copy `data/` onto `src/main/resources/data/`, replacing the 10 `*_armor_trim_smithing_template_duplication.json` recipes, which still use diamonds.
The generator `generators/trims.py` (`DUP` table) now writes the same recipes.
