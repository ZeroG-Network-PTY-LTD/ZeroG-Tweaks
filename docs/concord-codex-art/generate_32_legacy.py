"""Historical native32 study; use generate.py for the approved native64 production art.

Usage: python generate.py <runtime assets/zerog_tweaks directory>
No AI-sheet resampling. Uses locked repository ramps; does not alter lore or UI.
"""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'art-direction/generator'))
from style_kit import RAMPS

metal = RAMPS['moonsteel']
cyan = RAMPS['cerulite']
violet = RAMPS['glow']
pages = RAMPS['wood']
image = Image.new('RGBA',(32,32),(0,0,0,0))
d = ImageDraw.Draw(image)
# Three-quarter closed book: binding, lower cover, pages, upper cover.
d.polygon([(2,10),(5,7),(11,26),(10,30),(7,29),(2,14)],fill=metal[0])
d.polygon([(3,11),(5,8),(10,26),(9,29),(7,27),(3,14)],fill=metal[1])
d.line([(3,10),(4,9),(9,27)],fill=metal[3])
d.polygon([(10,26),(29,21),(29,27),(11,30),(9,29)],fill=metal[0])
d.polygon([(11,25),(28,21),(28,26),(11,29)],fill=pages[5])
d.line([(12,26),(28,22)],fill=RAMPS['solvanite'][5])
d.line([(12,28),(28,24)],fill=RAMPS['solvanite'][5])
d.line([(11,29),(28,25)],fill=pages[4])
d.line([(11,30),(29,26)],fill=metal[4])
d.polygon([(5,7),(23,2),(29,22),(11,27)],fill=metal[0])
d.polygon([(6,8),(22,3),(28,21),(12,26)],fill=metal[1])
d.polygon([(8,9),(21,5),(26,20),(13,24)],fill=metal[2])
# Quiet stepped navy cover bands, not noise/dithering.
d.polygon([(9,10),(20,7),(25,19),(14,22)],fill=metal[1])
d.line([(6,7),(23,2),(24,5)],fill=metal[4])
d.line([(7,8),(22,4)],fill=metal[3])
d.line([(12,26),(28,21)],fill=metal[3])
d.line([(27,18),(28,21),(25,22)],fill=metal[0])
# Silver L fittings with a dark rim and deliberately small cyan rivets.
for shape,shine,rivet in [
 ([(5,7),(9,6),(10,8),(7,9),(7,11),(5,10)],[(5,7),(8,6)],(7,8)),
 ([(20,3),(23,2),(25,6),(23,7),(22,5),(21,5)],[(21,3),(23,3),(24,5)],(23,4)),
 ([(25,20),(28,19),(29,22),(25,23),(24,21)],[(26,20),(28,20)],(27,21)),
 ([(10,23),(12,22),(14,25),(12,27),(10,26)],[(10,24),(12,23)],(12,25))]:
 d.polygon(shape,fill=metal[0])
 d.polygon(shape,fill=metal[4])
 d.line(shine,fill=metal[5])
 d.point(rivet,fill=cyan[4])
# Spine clasp and readable hinge bands.
for y in (12,19,25):
 x=3+(y-12)//3
 d.line([(x,y),(x+2,y-1),(x+3,y+1)],fill=metal[4])
 d.point((x,y),fill=metal[5])
d.polygon([(4,16),(6,14),(8,17),(6,19),(4,18)],fill=metal[0])
d.polygon([(5,16),(6,15),(7,17),(6,18)],fill=metal[4])
d.point((6,16),fill=cyan[5])
# Clear star chart: open negative space, a thin orbit and one unmistakable star.
d.line([(11,15),(12,12),(16,11),(21,12),(23,15),(21,19),(16,20),(12,18),(11,15)],fill=cyan[3])
d.line([(12,13),(13,12),(16,11)],fill=cyan[4])
d.line([(15,8),(19,8),(23,11),(25,15),(23,20),(20,22)],fill=violet[3])
for x,y in [(19,8),(23,20)]:
 d.point((x,y),fill=violet[5])
for x,y in [(19,9),(23,19)]:
 d.point((x,y),fill=violet[4])
for x,y in [(11,15),(21,19)]:
 d.point((x,y),fill=cyan[5])
d.polygon([(17,12),(18,14),(21,15),(18,16),(17,18),(16,16),(13,15),(16,14)],fill=cyan[4])
d.line([(15,15),(19,15)],fill=cyan[5])
d.line([(17,13),(17,17)],fill=metal[5])
d.point((17,15),fill=violet[5])

bounds=image.getbbox()
assert bounds and all(image.getpixel((x,y))[3]==0 for x,y in
    [(x,0) for x in range(32)]+[(x,31) for x in range(32)]+
    [(0,y) for y in range(32)]+[(31,y) for y in range(32)]), 'Cropping/padding failure'
assert image.mode=='RGBA' and image.size==(32,32)
assert len(image.getcolors())>=16,'Insufficient material shading'
assets=Path(sys.argv[1]); model={'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:item/concord_codex'}}
for folder in (HERE/'source',assets):
 (folder/'textures/item').mkdir(parents=True,exist_ok=True)
 (folder/'models/item').mkdir(parents=True,exist_ok=True)
 image.save(folder/'textures/item/concord_codex.png')
 (folder/'models/item/concord_codex.json').write_text(json.dumps(model,indent=2)+'\n')

# Native source and nearest-neighbour review only, never runtime downscaling.
preview=Image.new('RGB',(720,450),'#20232d');p=ImageDraw.Draw(preview)
p.text((20,15),'CONCORD CODEX - ACTUAL NATIVE 32x32 ART',fill='#dcecff')
preview.paste(image.resize((384,384),Image.Resampling.NEAREST),(20,45),image.resize((384,384),Image.Resampling.NEAREST))
p.text((450,60),'Inventory: 32 pixels',fill='#dcecff')
preview.paste(image,(485,100),image)
p.text((450,160),'Enlarged: 4x',fill='#dcecff')
large=image.resize((128,128),Image.Resampling.NEAREST);preview.paste(large,(450,190),large)
p.text((450,365),'Painted accents; no',fill='#b8c2dc')
p.text((450,383),'runtime light claim.',fill='#b8c2dc')
preview.save(HERE/'native-preview.png')
manifest={'size':[32,32],'mode':'RGBA','alpha_bounds':bounds,'palette':'locked moonsteel/cerulite/glow/wood/solvanite ramps',
          'source':'original native generator, not concept resampling','files':[]}
for rel in ('textures/item/concord_codex.png','models/item/concord_codex.json'):
 path=HERE/'source'/rel
 manifest['files'].append({'path':'assets/zerog_tweaks/'+rel,'source':'source/'+rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Native Codex authored, model bound and padding/material checks passed.')
