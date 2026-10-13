# Lunar survey outposts — approval draft

Status: owner requested a draft; layout, loot and generation settings NOT approved
or activated. This is not an implemented structure or a rendered Blockbench model.
Keep this distinct from the pending Meteor Maw impact-wreck concept.

## Proposed look

Small abandoned maintenance/survey sites, not a new Concord story chapter. Use
existing Lunar Stone Bricks and Mare Basalt for walls/foundations, Hoarwood for
doors/supports, ordinary Glass or Frost Glass for remaining windows, and Selenite
Lamps for occasional surviving illumination. No Star Glass, free functional
machines or new texture placeholders. Approved A/C art remains unchanged.

Damage is geometric: missing roof sections, fallen supports and uneven rubble.
Keep the door, chest and walking route readable. Blend the edge into actual local
regolith/grass instead of stamping a square lawn across ponds or cliffs.

## Three proposed variants

| Variant | Draft footprint | Features |
| --- | --- | --- |
| Field station | 11x13, height7 | One cracked shelter, small external sampling bench, one chest, damaged lamp mast |
| Fallen survey tower | 7x9, height9 | Short remaining tower, fallen mast beside it, open instrument alcove, one chest |
| Sample trench | 13x11, depth4 | Shallow shored pit, steps down, covered tool cache and small rubble piles |

Field-station plan (not a block-exact schematic):

```text
                 lamp mast
                     |
       +-----------------------+
       | cracked shelter       |
       | window  chest  window |
       |        clear aisle    |
       +----------door---------+
                  path
           sampling bench
             loose rubble
```

The sampling bench/instrument alcove is decorative block geometry, not a
machine with an invented GUI or processing contract. The pit must not contain
placed rare ore clusters or bypass the Ferrox/Moonsteel mining ladder.

## Loot proposal — still awaiting approval

- Local ordinary building materials: Lunar Stone/Regolith/Mare Basalt pieces.
- Small amounts of vanilla basic supplies such as torches, string, paper and
  copper/iron scraps. Exact IDs, weights and quantities remain unapproved.
- Never Dormant Wisp, Concord Codex, Broken Console, guardian keys, upgrade
  templates, rare Moon metals/gems or new story fragments.
- No automatic claim that these are the Maw's Concord debris or the Moon relay.

## Generation proposal — still awaiting approval

Rare random-spread sites: start by evaluating the existing ruin convention of
spacing40/separation20 chunks, not a guaranteed outpost near every gate. Keep
clear of arrival footprints and settlements; proposed96-block settlement buffer
needs implementation and testing before any guarantee can be made.

Select dry, moderate-slope terrain; grade only used foundations and paths, not a
whole surrounding lawn. Never overwrite containers, gates, inhabited builds or
water. Use proper structure starts/pieces so `/locate` and bounded chunk placement
can work. Do not implement this as an unchecked periodic player-nearby spawn.

## Approval and implementation checklist

- [ ] Owner approves variants, proportions and palette.
- [ ] Produce block-exact editable models/schematics and image references.
- [ ] Owner approves exact ordinary loot and generation settings.
- [ ] Register new structure IDs without renaming/removing existing IDs.
- [ ] Check actual terrain placement, chest access, rotations and protection.
- [ ] Ordinary-server natural generation evidence at multiple seeds.
- [ ] Add guide images and location instructions after verified implementation.

Until those decisions are approved, no code/data/JAR contains these outposts.
