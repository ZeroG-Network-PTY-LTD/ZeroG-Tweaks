"""Native32 Flux Wrench, authored from the approved9Oct sci-fi concept.

Run after full-art-rollout-v4; never downscale the concept sheet into a texture.
Usage: python generate.py <runtime assets/zerog_tweaks directory>
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'art-direction' / 'generator'))
from style_kit import RAMPS

metal, cyan, violet, gold = [RAMPS[k] for k in ('moonsteel', 'cerulite', 'glow', 'solvanite')]
sprite = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
d = ImageDraw.Draw(sprite)
# One coherent diagonal silhouette, open jaws facing the working end.
d.polygon([(3,26),(13,16),(13,12),(15,8),(21,2),(27,2),(28,4),
           (23,5),(20,8),(22,11),(25,11),(27,7),(29,6),(29,12),
           (24,17),(20,18),(8,29),(4,29)], fill=metal[0])
d.polygon([(4,26),(14,16),(14,12),(16,8),(21,3),(26,3),(23,4),
           (18,8),(21,12),(26,12),(28,8),(28,12),(23,16),
           (19,17),(7,28),(4,28)], fill=metal[2])
d.line([(4,25),(14,15),(15,11),(17,8),(22,3),(26,3)], fill=metal[4], width=1)
d.line([(5,25),(14,16),(16,12)], fill=metal[5], width=1)
d.line([(19,8),(22,12),(26,12),(28,9)], fill=metal[4], width=1)
d.line([(20,9),(23,13),(26,13)], fill=metal[1], width=1)
d.line([(22,16),(27,11)], fill=metal[3], width=1)
# Dark gripping surface and bevelled collar.
d.polygon([(5,25),(11,19),(14,22),(8,28)], fill=metal[1])
for x,y in [(6,25),(8,23),(10,21)]: d.line([(x,y),(x+2,y+2)], fill=metal[0])
d.line([(11,18),(15,22)], fill=metal[4], width=1)
d.line([(12,18),(15,21)], fill=metal[5], width=1)
# Recessed cyan circuitry along the shaft and inner jaw.
d.line([(13,18),(16,15)], fill=cyan[1], width=3)
d.line([(13,18),(16,15)], fill=cyan[3], width=1)
d.point((14,17), fill=cyan[5])
d.line([(20,7),(22,9),(24,9)], fill=cyan[3], width=1)
d.point((21,8), fill=cyan[5])
d.line([(6,27),(7,26)], fill=cyan[4], width=1)
# Violet socket: dark rim, saturated facets, pale specular core.
d.polygon([(15,13),(18,10),(21,13),(18,16)], fill=violet[0])
d.polygon([(16,13),(18,11),(20,13),(18,15)], fill=violet[2])
d.line([(16,13),(18,11),(19,12)], fill=violet[4], width=1)
d.point((18,12), fill=violet[5])
for x,y in [(16,9),(23,14),(5,27)]:
    d.rectangle((x,y,x+1,y+1),fill=gold[2]);d.point((x,y),fill=gold[4])

out = Path(sys.argv[1]) / 'textures' / 'item'
out.mkdir(parents=True, exist_ok=True)
sprite.save(out / 'flux_wrench.png')
sprite.save(HERE / 'flux_wrench.png')
sprite.resize((512,512),Image.Resampling.NEAREST).save(HERE / 'flux_wrench_native_preview.png')
print('Authored32x32 transparent Flux Wrench; handheld model and registry ID unchanged.')
