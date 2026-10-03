# Miniature planet bees — current vanilla-UV revision

Twelve families: Moon, Mars, Cerulon, Skarn, Eidolon and Solvane Glowbugs;
Flora, Midnight, Crimson, Tropical, Gold Dust and Magma Bees.
The six concepts follow the supplied reference palettes and motifs. Art is
original, not an extraction of the reference image or Mojang PNGs, and is not
claimed as a pixel-identical recreation of the concept render.

Runtime geometry and animation use Minecraft Java 1.21.1 BeeModel, including
antennae, stinger, six legs and symmetric wings. Adult rendering/hitboxes are
half vanilla size (.35 × .3 blocks); baby scaling remains vanilla on top of that.
64×64 painted atlases preserve the actual vanilla UV islands. Both 9×6 wing
faces are painted. Eight explicitly selected entity PNG frames cycle every
three ticks; blinking and emissive eye/wing masks are separate. Entity PNG
animation does not rely on mcmeta. There is no dynamic world light.

Matching hives have distinct top/side/front faces and honey-full drip animation;
combs use vanilla-like honeycomb silhouettes; bottles and viscous placeable
honey buckets are registered. Honey belongs to the hive family: vanilla AI
allows different bees to share a hive. Productive Bees integration, family-only
occupancy rules and species-specific processing recipes remain future work.

Homes: Flora/Tropical → Cerulon; Midnight → Moon; Crimson → Mars;
Gold Dust → Solvane; Magma → Skarn. Existing planet families stay on their
named planets, including Frost-style Eidolon bees. Rare occupied hives generate
with fertile patches in new chunks. Spawn eggs and low-weight natural spawns
are provided. Vanilla smoke protection, honey level/comparator, nectar return,
bee storage and Silk Touch occupant/honey preservation are retained.

240 PNGs and 60 editable projects. Bee projects are half-sized rig/UV studies,
not Java exports. Hives embed distinct face art; PNG animation is demonstrated
by the runtime renderer/resources, not certified by Blockbench import.
See `miniature_bees_uv_reference.png` and `miniature_bees_texture_animation.gif`.
These are offline references, not game captures or final human approval.

Generator: `docs/zero-g-tweaks-bundle/generators/planet_bees.py`.
Run after dimension_ecology.py; it intentionally supersedes 18 initial bug PNGs.
Before bytes, manifests and source hashes are retained. Code belongs to 1.21.x;
jar/test evidence belongs to Docs. No paid generation or canonical GLB claim.
