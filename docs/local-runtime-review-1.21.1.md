# Local 1.21.1 runtime review — unpublished

Prepared on `1.21.1-update`, based on `d13b7c14c45a09d5440810570e0231eac22abcb1`;
publication branch: `codex/full-collection-runtime-1.21.1`.
The human explicitly authorised committing/pushing this update on 2026-10-01.
No new jar has been copied to the CurseForge instance.

## Implemented code

- **80 wearable armour pieces:** 20 material registries, real equipment slots,
  durability, repair ingredients, enchantability, vanilla equipment attributes
  and right-click/dispenser equip behaviour. Existing item IDs are preserved.
- **100 functional tools:** 20 five-tool sets now use vanilla sword, pickaxe,
  axe, shovel and hoe classes, correct main-hand attack attributes, durability,
  mining behaviour, repair ingredients and enchantment tags. Existing IDs are
  preserved. Mining tiers are conservative vanilla equivalents, not the future
  planet progression gates.
- **Eight documented full-set ability portions:** Nullifite blocks fall damage;
  Moonsteel halves fall damage; Ruskite reduces fire damage by 25%; Skarnite
  blocks fire/lava damage; Eidolite blocks freezing damage; Cobaltium increases
  mining speed by 10%; Ferrox adds +1 total toughness; Astrium adds +2 max health.
  Only all four matching pieces activate bonuses. Attribute modifiers are
  transient, uniquely identified and removed when the set is incomplete.
- **Spawnable Tidewraith pair:** regular and boss entity registrations, vanilla-
  shaped recoloured spawn eggs, flying patrol/attack behaviour, synced/saved boss
  palettes, boss bar, authored animation controller names and client-only
  GeckoLib rendering. The boss retains its authored size, not six-times scaling.
  Stats are initial testing values, not final campaign balance.

**Tidewraith artwork is now imported with human approval.** The project-specific
Blockbench/GeckoLib-format exception and unverified concept-reference artwork
licence were explicitly accepted. The import receipt records source and output
hashes; it is not a canonical GLB admission certificate. Both authored geometries,
all 19 animation clips, five unchanged base PNGs and five matching glow masks are
included. Runtime controllers currently use flight, blink and mouth-open only.
The existence guard remains as a safety check; all 14 required resources are
present and both eggs/entities now register.

- **Layered deposits repaired:** ashfall, crater dust and snowpack now share
  vanilla eight-layer shapes, stacking and support rules. They do not melt next
  to lamps. Their existing blockstates and layer-count loot conditions now parse.
- **Wooden fences repaired:** Charwood, Gildwood, Hoarwood and Shardwood now
  register FenceBlock instead of WallBlock, matching the boolean connection
  properties in their existing models. Registry IDs and artwork are unchanged.

## Artwork versus equipment behaviour

The twenty new green-box Blockbench armour projects are in the design collection.
The gameplay pass currently uses the branch's existing vanilla-layer armour
textures. It has **not** mapped the new HD studies, animated PNGs or glow masks
onto the Java equipment renderer. Therefore source compilation does not prove
the worn result matches the new showcase. Orange-box geometry has not been
restored.

## Evidence and limits

- Baseline build passed.
- Equipment/source changes and opt-in regression tests compile against actual
  Minecraft 1.21.1 / NeoForge 21.1.252 / GeckoLib 4.9.3.
- Eight equipment/block GameTests cover all 80 armour pieces, all 100 tools, right-
  click equip, slot-bound protection, matching-set bonuses, modifier cleanup and
  eight-layer deposit shapes/stacking and wooden-fence connection states.
- Three preserved Tidewraith GameTests cover lifecycle/attributes, actual egg
  use and saved/clamped palettes. **All eleven required server tests passed** on
  this source base on 2026-10-01. Transcript:
  `20261001_111431_runZeroGTests.log` in the local review output folder. The three
  deposit loot parsing errors seen in the first nine-test run are absent after
  repair.
- A local-file reference audit found zero missing references across 3,193
  existing models, 878 blockstates and 4,169 texture references, before adding
  the two vanilla-template Tidewraith egg models. This is not GPU or UV testing.
- The full 609-presentation design catalogue was launched in Blockbench.
  Live viewport verification remains unavailable; source/static previews are
  not a claim of game-client rendering.
- The isolated server and opt-in client asset review ran with human approval,
  outside CurseForge. The final client review passed at 19:56 Asia/Bangkok on
  2026-10-01: both models baked, required flight/eye/mouth clips loaded, and all
  five base textures and five emissive textures uploaded. The wooden-fence model
  definition errors from the first client run are absent after repair.
  Transcript: `20261001_125538_runAssetReview.log`. This is not in-world artistic
  approval or a multiplayer/animation fit check.
  Existing client event-bus deprecation warnings are warnings, not build failures.

## Approved isolated test commands

Normal release build: `gradlew.bat build`.

Equipment test compilation only: `gradlew.bat compileJava -PzeroGTests`.

Equipment and Tidewraith test compilation only:
`gradlew.bat compileJava -PzeroGTests -PtidewraithTests`.

Isolated equipment and Tidewraith tests run with
`gradlew.bat runZeroGTests -PzeroGTests -PtidewraithTests`. The test game directory is
`run-local-zerog-tests`, separate from CurseForge worlds. Test classes and
templates are opt-in and are not intended for normal release jars.

Client resource review: `gradlew.bat runAssetReview -PclientReview`. It closes its
own isolated client after logging `ZEROG_CLIENT_ASSET_REVIEW_PASS` or `_FAIL`.
Check that marker; a clean launcher exit alone does not prove the checks passed.

## Still unfinished

New HD worn-armour mapping, animation/emissive renderer, remaining set abilities,
smithing upgrades, planet-specific mining gates; all other creature AI/runtime
registrations; accepted vanilla-style bees and Productive Bees integration;
functional machine menus, FE/recipe processing, controller/multiblock validation,
frame/bee/comb/genetic slots; natural Tidewraith spawning, campaign boss phases
and approved drops; client visual/animation checks and release installation.

This is a partial implementation and review candidate, not a finished mod.
