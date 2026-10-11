# Buried Observatory — desert Concord ruin

Two original 21×11×21 observation rooms now route the existing Buried Observatory loot table through a dedicated desert structure. Existing Sunbaked Stone Bricks, cracked bricks, Ruinstone, hull plating and Crystal Glass form a low room with four instrument plinths and a roof lens. Supported exterior Rustsand dressing gives partial burial without sand falling into the room. One variant has a damaged rear roof corner.

A three-block north doorway leads along a continuous floor to one north-facing chest at(10,2,15), with clear lid space. Its existing Star Map Fragment pool and all other loot probabilities are unchanged. Existing planetary mine chests that use this table are preserved; those mines are not themselves dedicated Observatories.

Approved lore says this place leads to a hidden planet. This batch supplies the existing fragments, but does **not** invent coordinates, a hidden destination, logs, dialogue or new quest rules. Full hidden-planet discovery remains pending an approved contract.

## Where to inspect it

Dune Seas, Mesa Canyons and Salt Flats are eligible. The ordinary dry-ground jigsaw route retains six-block terrain tolerance, bounded nearby search32 and `always_place=false`. Random spread spacing40/separation20 is a placement grid, not a guaranteed density or distance to spawn.

Explore newly generated desert terrain, or use the operator locator:

```mcfunction
/execute in zerog_tweaks:g2_p2 run locate structure zerog_tweaks:buried_observatory
```

No hub reset or existing planetary-terrain replacement is part of this update. Manual placement alone does not establish natural generation.

## Verification and remaining work

Static contracts check permitted original palettes, registered desert biomes, source/runtime template bytes, exactly one correct chest and bounded placement. A focused gameplay test checks both variants in four rotations, physical chest/lid, approach headroom/floor and actual Star Map Fragment loot. Natural ordinary-world placement is checked separately.

The required gameplay test passed all eight placements in1.317s, with normal server shutdown (`20261011_091025_runWorkflowTests.log`, total1m22). Two static contracts pass, including solid support directly below every Rustsand dressing block. Native ZeroG tests omit optional Productive Bees/orbital addons and do not certify the full modpack.

Client appearance, sand/terrain blending, every variant in ordinary worlds, broader seeds and full hidden-planet progression remain pending. Sunken Relay and Sunken Lab remain the missing dedicated ruins. No undefined biology, endings or later crafting costs are guessed.

Ordinary fresh seed-zero `g2_p2` generation found the site at locator X/Z272/304, start chunk17/19. Saved inspection confirms49FULL chunks and one natural jigsaw piece. Of three unopened chests using this loot table in the area, one is inside the Observatory's recorded piece bounds, at241/70/314; the nearby mine loot remains separate. The helper now reports this geometric association explicitly, without claiming actual loot rolls from unopened natural chests. [Natural report](reports/natural-buried-observatory-20261011.json). Temporary force loads were removed before save and normal shutdown; transcript `20261011_091254_runServer.log`,2m14. One site is not statistical rarity or all-biome proof.

Clean build passed in44s (`20261011_091155_clean.log`). Asset audit:8021models,1529blockstates,4005PNGs,130animation metadata files, zero errors. All six new resources match the clean JAR and optional GameTest entries are absent; three manufacturing source/JAR contracts still pass.

The same-version `1.0.12-dev` JAR is installed with an old-JAR backup, while Minecraft was closed. Hub, player saves and dependencies are preserved. [Installation receipt](reports/buried-observatory-install-20261011.json) · [asset audit](reports/buried-observatory-assets-20261011.json) · [published JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-buried-observatory-20261011.jar). SHA256 `8d89f1900cc840c0e22fa918963ff032834f4174531054eb5ea6bf6f832ab1e0`.

[Editable generator](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/wasteland-ruins/generate_buried_observatory.py) · [route graph](reports/buried-observatory-routes-20261011.json).
