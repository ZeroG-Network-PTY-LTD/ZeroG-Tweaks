"""Generate a small local gallery for the current additions, retaining legacy rosters."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[3]/'docs/asset-collection-1.21.1'
revisions={'crystals-amethyst-style-v2':('Crystals, ingots/raw materials and Star Glass',['crystals_v2_preview.png','animated_updates.gif']),
 'dimension-ecology-v1':('Planet soil, farmland, flora and fluids',['dimension_soils_reference.png','dimension_fluids_reference.gif']),
 'miniature-planet-bees-v1':('Current half-size bees, hives and honey',['miniature_bees_uv_reference.png','miniature_bees_texture_animation.gif']),
 'planet-blazes-v1':('Cosmic vanilla-rig Blazes and rods',['planet_blazes_reference.png']),
 'vanilla-liquid-buckets-v1':('Current exact vanilla-base liquid buckets',['vanilla_bucket_reference.png'])}
page=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ZeroG current additions</title><style>body{background:#151d2a;color:#ecf0fb;font:16px system-ui;max-width:1200px;margin:32px auto;padding:16px}a{color:#8bddff}img{max-width:100%;image-rendering:pixelated}ul{columns:3}li{break-inside:avoid;margin:8px 0;overflow-wrap:anywhere}@media(max-width:700px){ul{columns:1}}</style><h1>ZeroG current additions — 1.21.1</h1><p>Offline authored texture references and editable projects, not in-game screenshots. Java runtime uses vanilla Bee/Blaze rigs. No client visual approval or dynamic-light shader claim.</p><p><a href="https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/README.md">Current documentation / development jar</a> · <a href="review.html">Historical catalogue</a></p>']
for folder,(title,images) in revisions.items():
    page.append('<h2>'+title+'</h2><p><a href="'+folder+'/README.md">Notes and limits</a></p>')
    for name in images:page.append('<img loading="lazy" src="'+folder+'/'+name+'" alt="'+escape(title)+'">')
    projects=sorted((ROOT/folder/'blockbench').glob('*.bbmodel'))
    if folder=='dimension-ecology-v1':projects=[p for p in projects if not p.stem.endswith('_glowbug')]
    page.append('<details><summary>'+str(len(projects))+' editable projects — open one at a time in Blockbench</summary><ul>')
    page.extend('<li><a href="'+folder+'/blockbench/'+escape(p.name)+'">'+escape(p.stem)+'</a></li>' for p in projects)
    page.append('</ul></details>')
page.append('<p>The six initial ecology bug studies are retained for provenance but omitted here, superseded by the current bee revision. Legacy catalogue hashes are unchanged. Entity PNG animation and emissive support are runtime features; bind-pose project files are not proof of client rendering.</p></html>')
(ROOT/'additions-review.html').write_text('\n'.join(page),encoding='utf-8')
print('Current additions gallery written.')
