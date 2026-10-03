"""Generate the local HTML view without rewriting the historical catalogue."""
from html import escape
from pathlib import Path
import json

root = Path(__file__).resolve().parents[2] / 'asset-collection-1.21.1/crystals-amethyst-style-v2'
manifest = json.loads((root / 'manifest.json').read_text())
projects = sorted((root / 'blockbench').glob('*.bbmodel'))
cards = ''.join(f'<li><a href="blockbench/{escape(p.name)}">{escape(p.stem)}</a></li>' for p in projects)
textures = ''.join(f'<figure><img src="textures/{escape(t["path"])}" alt="{escape(t["path"])}">'
                   f'<figcaption>{escape(t["path"])}</figcaption></figure>'
                   for t in manifest['textures'] if t['size'] == [32, 32])
page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZeroG — new crystals, metals and Star Glass</title>
<style>body{background:#151d2a;color:#ecf0fb;font:16px system-ui;max-width:1200px;margin:32px auto;padding:16px}
a{color:#8bddff}img{max-width:100%;image-rendering:pixelated}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
figure{margin:0;padding:12px;background:#202b3b}figure img{width:96px}figcaption{overflow-wrap:anywhere;font-size:13px}li{margin:6px 0}</style>
<h1>ZeroG crystal/material update — Minecraft 1.21.1</h1>
<p>96 texture PNGs · 80 editable Blockbench projects. Offline references, not in-game screenshots.
The historical catalogue remains unchanged. Runtime code is on 1.21.x; jar and player guide are on Docs.</p>
<p><a href="https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/crystal-material-update-1.21.1.md">Current candidate and installation guide</a>
 · <a href="../review.html">Historical full collection</a> · <a href="README.md">Notes and limits</a></p>
<h2>Star Glass and crystal growth</h2><img src="animated_updates.gif" alt="Offline Star Glass animation reference">
<p>Light: crystal stages 1/2/4/5; Star Glass 12. Three colour states, sixteen 64px frames, 3 ticks each.
Blockbench glass displays frame zero; runtime mcmeta animates it.</p>
<h2>Planet Star Sands</h2><img src="planet_sands_reference.png" alt="Six sands that smelt to Star Glass">
<h2>Sixteen ingot/raw-metal pairs</h2><img src="ingots_raw_reference.png" alt="Modern vanilla-style metal inventory sprites">
<h2>Editable models</h2><details><summary>Open one project at a time in Blockbench</summary><ul>PROJECTS</ul></details>
<h2>Native 32px texture roster</h2><section>TEXTURES</section>
<p>Grayscale Brine/Frost/Prism textures are tinted in-game. Displayed source tiles are not their final dimension colour.
Star Glass uses translucent pane art, not a parallax shader. Sand registration/furnace recipes are present; modpack visual validation remains pending.
<a href="../additions-review.html">Current soil, fluid, miniature bee and cosmic Blaze additions</a>.</p>
</html>'''
(root / 'review.html').write_text(page.replace('PROJECTS', cards).replace('TEXTURES', textures), encoding='utf-8')
print(f'Gallery written with {len(projects)} project links: {root / "review.html"}')
