# Native precipitation and harsh storms — 1.0.10

The approved green acid rain means falling rain sheets and droplets, not dust.
Use Minecraft 1.21.1's existing rain texture with green vertex tint, roof-clipped
columns, distance fading, scrolling UVs and green native splash particles.
Do not replace vanilla rain globally or recolour the Overworld. Snow uses the
native snow texture. No new texture, Blockbench geometry or third-party art is
required for this correction; all existing vine/sky/model sources remain intact.

Harsh electrical storms now require genuine server-owned Minecraft lightning
entities: visible branched bolts, thunder and normal strike interactions. This
supersedes the 1.0.9 cosmetic-only lightning design. Acid damage and poisonous
vine damage remain deferred. Storm skies darken and obscure the bright panorama
and stars; native clouds appear during precipitation, while optional Iris
volumetric clouds consume the synchronized rain/thunder strengths.

The creative tester controls weather for the occupied planet, not just its own
client. Actual lightning can damage entities and ignite blocks where Minecraft
rules permit; protected test arrival gates reject nearby lightning strikes.
Weather controls do not modify the Overworld. Broader flora artwork stays later
work. In-game visual approval and shader compatibility are still player checks.

Implementation belongs exclusively on 1.21.x; player guide/JAR/checksums on Docs.
