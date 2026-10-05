# Survival travel and Sol structure source

This implementation is separate from the historical unlimited-power T6 test-hub gates. It preserves their layout and `zerog_planet_gates` SavedData. Player-built controllers now use a real block entity, FE storage, four recoverable upgrade slots and a paginated star chart; do not describe a compiled screen as visually approved.

## Coordinates and progression

The centre is pad-floor Y=0, with the controller at `(0,1,-2)` relative to the centre. These local coordinates rotate with the controller's horizontal facing. Tiers add frame rings at Y=-1, radius 2 through 7, respectively Nullifite, Moonsteel, Cerulite, Skarnite, Eidolite and Solvanite. Inner rings remain during upgrades. Pad widths are 3,3,5,5,7,7; existing inner pylon corners stay occupied instead of requiring conflicting pad blocks.

T1 has four two-block-high pylons and one port `(2,1,0)`. T3 adds a second port `(-2,1,0)` and a second pylon set. T5 adds two ports `(0,1,±3)` and a third pylon set. Pylons get taller with upgrades. Each tier from T2 adds its own standing arch along its positive-Z perimeter; the top is Y=2×tier, with a Lens Housing above it. The original T2 arch remains. T2 also requires a Selenite Block at `(0,6,3)` and an Aresite Block at `(0,-2,0)`. The Preview action marks missing next-tier components with particles; it does not create blocks or consume inventory.

The server revalidates formation, destination, ownership, energy and passengers. Breaking an outer component lowers the formed tier. Tier base costs are 500k/1M/3M/8M/20M/50M FE. Same-galaxy trips cost 25%, extra players add 10% each, and a Refracting Lens reduces cost by 20%. These are integer calculations to avoid floating-point one-FE rounding errors. FE capacity is twice the configured tier base cost. Charge rate is 1,000 FE/t doubled each tier; Cryo Core doubles this again. Multiple capability calls cannot bypass the per-tick limit.

T1 reaches Moon/Mars and return Overworld. Each next tier opens the next galaxy; aggregated moon destinations require T6. Capacity is 2/2/4/4/8/8 players, with +2 for a Capacity Coil. Upgrades have 1/1/2/2/3/4 active slots. Inactive items remain recoverable; destroying the controller drops upgrade contents.

Engage starts a 100-tick ready countdown. The initiator confirms automatically; other passengers must select Ready in the controller or step off to cancel. Any change in pad membership cancels the trip. Tamed pets belonging to passengers and passenger-leashed mobs on the pad travel; hostiles and item entities do not. Particles provide a launch effect, but a dedicated full-screen transition/loading animation is not implemented by these files.

First arrival constructs a small, dry, elevated T1 return platform from existing landing blocks. A crystal cell beneath its centre trickle-charges 1,000 FE/s; the return destination is the originating controller, not a guessed Overworld spawn. Recall Anchor binds to an owned formed controller, costs 150% of normal travel energy from that home buffer, and has a configurable default 1,200-tick cooldown. Group Anchor includes scoreboard teammates within eight blocks, within gate capacity. Third-party claims/team integrations are not claimed complete.

Planet gravity uses a transient vanilla gravity modifier, fixed to the approved six values with common configuration overrides; seeded wasteland values remain 0.6–1.3. It is removed outside ZeroG. Codex Moon/Mars pages are unlocked on recorded arrival, preserving the approved Concord story.

## Mars structures

`generate_sol_structures.py` generates two crashed hull layouts and one Aresite shrine from approved existing Martian Stone, Hull Plating, Corroded Hull, Olympium Plating and Broken Console blocks. No new textures or block/item IDs are fabricated. Rigid surface-jigsaw templates explicitly clear the volume, blend beard-box foundations and reject unsuitable wet/steep terrain through the existing dry-land jigsaw type.

The Mars wreck uses the existing `chests/mars_crash_site` loot table with Ferrox, Moonsteel and Olympium templates. The shrine guarantees one Aresite core and a Concord Codex, plus existing crash-site salvage. Natural placement is sparse: wreck grid spacing 40 chunks/separation 20, shrine 56/28, with additional terrain rejection. Biome tags list only Rust Plains/Oxide Badlands and, for wrecks, Polar Caps.

The source generator and generated copies live on Design; live NBT/data live on `1.21.x`. Run it with `--resources <code-checkout>/src/main/resources`. Generated structure presence is not proof of a surveyed planet. Isolated tests and actual client inspection must be reported separately.
