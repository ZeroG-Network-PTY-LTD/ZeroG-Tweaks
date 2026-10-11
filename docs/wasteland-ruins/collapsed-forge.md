# Collapsed Forge: small Concord smithy ruin

Original17×8×19 ruin implementing the Galaxy3 tracker's approved volcanic forge reward route. Two roof/wall damage variants, Scoria foundation, Scorched Marble supports, Charwood beams/workbench, cold blast furnace, anvil, lamp and one accessible chest. Existing `chests/collapsed_forge` rewards are unchanged. No new smith dialogue, machinery contract or boss encounter.

Dry-land jigsaw placement targets the three Skarn biomes and volcanic wasteland ash/basalt biomes. Initial40-chunk spacing/20 separation,6-block terrain-height tolerance and32-block bounded search. Lava-lake biome is excluded; no forced placement on failed terrain checks.

Generator: `generate_collapsed_forge.py --resources <code resources>`. Runtime and Design templates are produced together. Ordinary natural discovery, rarity balance and client appearance remain separate from template/loot tests. Existing explored chunks and hub are not regenerated.
