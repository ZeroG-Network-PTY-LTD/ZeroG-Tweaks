# Contributor reconciliation — 7 October 2026

The local runtime checkout was fast-forwarded from `48271c1f` to `d50eaade`.
These are real code commits, not Design previews. They will be included in the
next verified same-version build; pulling them alone does not update an installed JAR.

| Commit | Verified subject |
| --- | --- |
| `95615d89` | Moonsteel tools held right way up |
| `e2f646bd` | Sol block properties, Highlands spawns, gate launch and transition screen |
| `595c5fa2` | Axe stripping for ZeroG woods |
| `26b0ae2a` | Moonsteel axe, hoe and pickaxe heads face forward |
| `ec74b61c` | Moonsteel and Olympium 3D armour restored |
| `88cc2854` | Ironfall Meteor Maw Cinder Mite adds |
| `f79dcae2` | Cinder Mite bite no longer ignites the player |
| `614864fa` | Nullifite and Ferrox join the four Sol 3D armour sets |
| `26f9d9d6` | Nullifite, Ferrox and Olympium 3D tools |
| `b9205a41` | Black mob rendering repair: glow layer omitted without a glowmask |
| `92d2e2f5` | Sol metal block properties restored |
| `a8e91a4e` | Prism Sentinel sounds |
| `d732eb65` | Liquid-tab test expects twenty buckets including jelly |
| `d50eaade` | Three families of ore sounds |

The supplied label for `b9205a41` described a name change, but the actual commit
repairs six mobs rendering black. Runtime armour changes are retained according
to the updated code-branch `AGENTS.md`: four Sol sets use 3D shells; the remaining
sets keep vanilla-fit geometry. No other shells are reactivated.

## Sol tracker and remaining lore

[The Design HTML](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/sol-build-tracker.html)
was last changed by `8a37d472`. Its authored count is **32 of 42 done**.
The local Design checkout also received its matching generators and trackers,
without merging Design history into code.

The tracker predates several code commits above. Highlands spawns, travel polish,
Cinder Mites and metal-property repairs now have code, but physical client approval
is separate. Do not automatically mark all 42 entries complete from a successful build.

Still-open story tasks:

- Small hand-cut Aresite core shrine in every Rustborn settlement; retain the large
  standalone shrine and its Codex reward.
- Move Moon/Mars Codex page text out of hardcoded Java into translation keys.
- Define the approved form of Concord debris carried by Meteor Maws, without
  inventing new lore or registry IDs.
- Playtest the complete survival Sol loop, black-mob fixes and Moonsteel in both
  hands, first/third person and item frames.

No world regeneration, hub replacement or survival-cost changes belong to this batch.
