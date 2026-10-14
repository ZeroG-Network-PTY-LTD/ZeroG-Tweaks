# Direct-ingot Industrial Compressor

Owner14October contract:2ingots + reusable Plate Press ->1compressed plate;
4ingots + reusable Cog Press ->1cog. All22existing material families, including
vanilla Copper, have both routes. Press items stay in the catalyst/die slot.
Removed42crafting-table component recipes; they remain recoverable in Git.
Generators no longer recreate those routes. Recipe unlocks now point to pressing.
Existing base FE/time defaults remain2000/100ticks and4000/160ticks respectively.

Auto item routing on all five non-front faces exposes ingots, reusable die and
products. Input/die extraction is blocked; only products extract. Explicit
Reagents/Catalyst/Products/Off side settings remain available. All five faces
accept FE when enabled; front/null stay blocked and stale rotation handlers revoke.

Open-chamber native geometry uses existing original navy machine and terminal
textures with silver reinforcement. Two new recessed reusable-die models and
registered client renderer show ram movement, die, input squash and result preview.
Server-authored visual state sends only count-one display items/progress/duration,
not inventory/filters; visual previews never produce items. Update cadence is at
most every5successful work calls plus inventory/start/reset changes. Stalled work
does not keep advancing the piston. Client appearance remains unverified, not an
exact image match or a newly authored HD texture atlas.

Oxygen-assisted higher-stage pressing/tank requirements are future TODO only;
no invented oxygen costs, gas ports or recipe strength changes activated.
All20required isolated owner-followup checks passed, including all four facing
orientations/five non-front faces, real lines, exact processing/FE, reusable dies,
reload, no loaded bench route and visual-tag round trip without inventory mutation.
Normal build/packaged checks pass:44 correct recipes, no bench component files,
registered renderer present and no test classes shipped. Installed same1.0.12-dev
JAR while client closed with old-JAR backup; dependencies and saves preserved.
SHA256:4fcff84a1885a9e2b32e85ab93853c6f966827af333d5b3bc246155657d83f85.
Existing input plates can be recovered manually; they are no longer cog feedstock.
In-client animation, item/die scale and detailed concept resemblance await review.
