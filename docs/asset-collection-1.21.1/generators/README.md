# Authoring scripts, not a self-contained build tool

These scripts record the local authoring and packaging workflow. They refer to earlier local study outputs, helper modules, the supplied design packs and immutable repository commits. They are not claimed to run from this folder alone.

The green-box armour authoring script reads geometric facts from a locally constructed Minecraft 1.21.1 reference. That reference and the extracted Mojang source/pixels remain local and are deliberately not included here. All packaged armour textures and the player-study skin are independently painted procedural textures.

The packaging script uses native Windows file-copying to avoid WSL filesystem overhead. It preserves source projects and assembles generic-format, multi-texture inspection scenes without texture downscaling. Its command-scoped Git trust setting names only the source checkout. Neither it nor the showcase projects installs or registers anything in a Minecraft runtime.

Use the packaged individual models, textures, preview images, hashed catalogue and category showcases for review. Runtime integration, animation-renderer support and client verification remain separate work.
