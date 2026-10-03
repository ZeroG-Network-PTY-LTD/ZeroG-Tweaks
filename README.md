# ZeroG Tweaks — Minecraft 1.21.x development

NeoForge **1.21.1**, Java **21**, GeckoLib **4.9.3**. This is an unfinished
development build, not a shipped release or proof of modpack compatibility.

Current candidate: **1.0.1-dev**. Includes the latest Cerulon terrain/mob work,
four amethyst-style budding crystal families, animated light-12 Star Glass,
six planet Star Sands and updated crystal/ingot/raw-metal artwork.
See the [illustrated update and installation guide](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/crystal-material-update-1.21.1.md).

- [Full illustrated documentation and descriptions](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/README.md)
- [Armour, Bees, materials, mobs, eggs and drops gallery](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/current-collection-guide-1.21.1.md)
- [Blockbench design collection](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/asset-collection-1.21.1)
- [Multiblock controls and limits](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/multiblock-reference-guide.md)
- [Build and test evidence](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/verification-1.21.1.md)
- [Development jar and SHA-256](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Docs/docs/jars)

Implemented: 80 functional armour pieces, 100 tools, eight partial full-set
bonuses, approved regular/boss Tidewraith pair, deposit/fence repairs, and a
G-key guide for eight apiary structures: layers from Y=0, rotatable views,
coordinates and quantities. Genetics/cryo are separate external modules.

Still unfinished: HD worn-armour rendering, remaining creature gameplay,
Productive Bees integration, machine processing/menus, multiblock formation,
world ghost previews and natural Tidewraith spawning/boss phases/approved loot.

Build: `./gradlew build` (Windows: `gradlew.bat build`). Optional server tests:
`gradlew.bat runZeroGTests -PzeroGTests -PtidewraithTests`. Optional client review:
`gradlew.bat runAssetReview -PclientReview`. These launch isolated Java development
instances, not the user's CurseForge modpack. Test sources are excluded from
normal jars. Do not launch game tests without current user direction.

Branch ownership: code/build/runtime resources on `1.21.x`; art and generators
on `Design`; documentation/images/jars on `Docs`; shipped code only on `Released`.
Never merge Design/Docs histories into code or vice versa. Never commit directly
to Released, force-push, or delete branches/tags.
