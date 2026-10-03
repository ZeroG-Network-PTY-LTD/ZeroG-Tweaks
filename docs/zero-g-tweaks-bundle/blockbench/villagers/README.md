# Planet villagers: six custom species

One villager species per fixed planet, each with its own model. Sheets are in `sheets/villagers/` (`00_overview.png` plus one sheet per species).

| Species | Entity id | Planet | Signature profession | Job site |
| --- | --- | --- | --- | --- |
| Lunari | `zerog_tweaks:lunari` | Moon (0.5 g) | Regolith Refiner | `ore_refinery` |
| Rustborn | `zerog_tweaks:rustborn` | Mars (0.7 g) | Rust Mechanic | `combustion_generator` |
| Glintfolk | `zerog_tweaks:glintfolk` | Cerulon (0.9 g) | Crystal Tender | `crystal_growth_chamber` |
| Ashwrights | `zerog_tweaks:ashwright` | Skarn (1.2 g) | Ashwright Smith | `alloy_forge` |
| Hollow Kin | `zerog_tweaks:hollow_kin` | Eidolon (0.8 g) | Salvager | `salvage_station` |
| Sunwardens | `zerog_tweaks:sunwarden` | Solvane (1.3 g) | Sun Keeper | `solar_array` |

All six entity ids are **new**. Nothing existing is renamed or removed. The clothing overlays in
`docs/planet-worldgen-overhaul/source/villagers/` stay as they are, for vanilla villagers that travel through a gate.

## Files per species (`<id>/`)

| File | Use |
| --- | --- |
| `<id>.geo.json` | GeckoLib / Bedrock geometry (format 1.12.0, box UV). Opens in Blockbench as a GeckoLib or Bedrock entity. |
| `<id>.animation.json` | `idle`, `walk`, `no` (head shake on a refused trade), plus the species extra (`halo_spin`, `goggles_down`, `work`, `dawn_hymn`). |
| `<id>.png` | Main texture, default biome. `<id>_<biome>.png` are the other two biome variants (VillagerType). |
| `<id>_glowmask.png` | Emissive layer (crystals, lamps, eyes, ember cracks, halo). |
| `professions/<profession>.png` | Profession overlay, same UV. It only repaints the species' accent pixels (stripe, scarf, shirt, apron trim, sash) in the profession colour. There are 13 vanilla professions plus the signature one. |

Copy into the mod as:
`assets/zerog_tweaks/geckolib/models/entity/villager/<id>.geo.json`,
`assets/zerog_tweaks/geckolib/animations/entity/villager/<id>.animation.json`, and
`assets/zerog_tweaks/textures/entity/villager/<id>/...`.

## Rules every species keeps

- Vanilla bone names: `head`, `body`, `arms`, `right_leg`, `left_leg`, plus `nose`/`hood`/`hat`-style children of the head.
- Crossed arms at -43 deg X, the same as the vanilla villager.
- Hitbox 0.6 x 1.95 and render scale 0.9375, so they fit 1 x 2 doors and village beds and work stations.
- Gravity sets the build: low gravity means long legs (Lunari, 14 px); high gravity means short and broad (Ashwrights 9 px, Sunwardens 10 px).

## Code notes (for the `1.21.x` branch)

1. `PlanetVillager extends Villager`, and each species registers its own `EntityType<PlanetVillager>`. Copy vanilla villager attributes, then apply the per-species changes from the sheet: Ashwrights 0.85x speed, 0.6 knockback resistance and fire immune; Hollow Kin immune to freezing.
2. Override `getBreedOffspring` so a child is the same species. For zombie conversion, use the vanilla zombie villager for now and keep the trade data.
3. Register six `PoiType`s on the machine blocks and six `VillagerProfession`s for the signature trades. The trades are in each sheet; every listed item id exists in `ItemInit`.
4. Renderer: `GeoEntityRenderer` with layers for the biome texture, glowmask (`AutoGlowingGeoLayer`), and profession overlay. Turn the head bone toward the look target.
5. Use the GeckoLib default `entityCutoutNoCull` render type. The Hollow Kin hood needs it so the inside shows through the face opening.
6. Biome variants: map each planet biome to the variant texture (see each sheet's Biome Variants panel).

Generator: `generators/villagers/overview.py <out_dir>` rebuilds all sheets, models, textures and overlays. Species are defined in `species.py`.
