# Compressor chamber lighting and die scale

Owner confirmed the machine processes correctly, but photographed dark internal
dies/ingots/cogs and a tiny die. No recipe, inventory, power or transfer rules are
changed by this repair.

The block-entity renderer used packed light from the opaque machine cell for its
contents. It now samples the open front's light, retains that sky-light component
and clamps displayed chamber block light to at least10. This is local render
illumination, not a world light-emitting block or a new FE-consuming lamp.

| Display | Previous | Repaired |
| --- | --- | --- |
| Die scale |0.48 with inherited FIXED transform|0.80 with NONE context|
| Die centre height |0.30|0.325|
| Ingot/result scale |0.45|0.60|
| Ingot/result centre height |0.345|0.40|
| Ram travel amplitude |0.30|0.25|

The12/16-wide die at0.80scale occupies0.60blocks inside the0.625block chamber.
Its base is above the existing press bed and its top below the fully descended
ram. A source-bound regression reads actual renderer constants and checks die
width/clearance plus101ram/shaft samples. Both checks pass; the Java build passed.
These are not GPU tests. Owner client review of brightness, material colour,
Iris/shader behavior, die size and pressing appearance remains required.

Do not restore FIXED here or copy inventory scaling into the chamber. Use NONE
and explicit chamber transforms; inventory artwork/display transforms remain
unchanged. Already placed compressors update on a normal client restart. No hub
regeneration, save changes or new server tests are needed for unchanged processing.

Same-version JAR installed with old-JAR backup while client closed. Archive:
`jars/zerog-tweaks-1.21.1-1.0.12-dev-chamber-light-20261014.jar`.
SHA256: `0c1375d42d8111b8e86cc808ef4deb7db512c1557df46b37b782b74c8d122dd5`.

## Owner review — 14 October

Owner reports "compressor passed". Processing, lighting and die/item scale are
accepted. A remaining visual delay between ram descent, showing the finished
plate/cog and ram lift is explicitly deferred until after the usage reset.
Repair the visual sequence later without generating outputs before the server
completes the recipe or changing ingredients/FE/die preservation. Check paused
jobs and cycle boundaries, then seek client timing approval. No new JAR or save
changes were made for this TODO update; work stops until the owner resumes.
