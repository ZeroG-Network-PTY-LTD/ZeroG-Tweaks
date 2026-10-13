"""Native64 Codex redraw. New one-pixel bevels, fittings, pages and chart detail.
No 32px texture or generated concept is resized into this source.
Usage: python generate_hd.py (review-only output under hd64/).
"""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'art-direction/generator'))
from style_kit import RAMPS
m=RAMPS['moonsteel'];c=RAMPS['cerulite'];v=RAMPS['glow'];w=RAMPS['wood'];cream=RAMPS['solvanite'][5]
im=Image.new('RGBA',(64,64),(0,0,0,0));d=ImageDraw.Draw(im)
# Native64 binding and paper block: complete geometry is drawn on this canvas.
d.polygon([(7,18),(12,14),(24,51),(24,59),(21,61),(14,57),(6,28)],fill=m[0])
d.polygon([(8,20),(11,17),(21,51),(21,58),(15,54),(8,27)],fill=m[1])
d.line([(8,20),(10,18),(20,52)],fill=m[3])
d.line([(8,26),(16,53),(19,56)],fill=m[2])
d.polygon([(22,51),(56,41),(59,45),(59,55),(25,62),(21,59)],fill=m[0])
d.polygon([(24,51),(57,42),(57,53),(24,60)],fill=w[5])
d.polygon([(25,51),(55,44),(55,50),(25,57)],fill=cream)
for y in (52,55,58):d.line([(25,y),(56,y-8)],fill=w[4])
for y in (53,56):d.line([(26,y),(55,y-7)],fill=cream)
d.line([(25,60),(58,53)],fill=m[3])
d.line([(26,61),(58,54)],fill=m[5])
# Cover and inset: cool hue-shifted clustered bands, not a noisy flat recolour.
d.polygon([(12,14),(46,5),(59,44),(25,54)],fill=m[0])
d.polygon([(13,15),(45,7),(57,43),(26,52)],fill=m[2])
d.polygon([(17,19),(43,12),(53,41),(28,47)],fill=m[1])
d.line([(15,16),(44,8),(55,42),(27,50),(15,16)],fill=m[3])
d.line([(15,15),(44,7)],fill=m[5])
d.line([(17,18),(43,11)],fill=m[2])
d.line([(28,49),(54,42)],fill=m[4])
# Fine embossed lower band retains quiet space around the constellation.
d.line([(28,45),(36,44),(43,42)],fill=m[2])
d.line([(20,21),(23,29)],fill=m[2])
# Individually bevelled silver corner fittings, with thin rims and inset rivets.
fittings=[
 ([(11,14),(21,11),(23,15),(16,17),(18,23),(13,25),(10,17)],
  [(12,15),(20,13),(21,15),(15,17),(17,22),(14,23),(12,17)],[(12,15),(19,13)],(17,15)),
 ([(40,6),(46,4),(49,7),(52,15),(47,17),(44,10),(42,10)],
  [(42,7),(46,6),(48,8),(50,14),(48,15),(45,9),(43,9)],[(42,7),(46,6),(48,8)],(46,9)),
 ([(51,40),(57,38),(60,44),(50,47),(49,43)],
  [(52,41),(56,40),(58,44),(51,45),(51,43)],[(52,41),(56,40),(57,42)],(54,43)),
 ([(22,47),(26,45),(31,51),(26,55),(23,53)],
  [(24,48),(26,47),(29,51),(26,53),(24,52)],[(24,48),(26,47),(28,50)],(26,50))]
for outer,inner,edge,(x,y) in fittings:
 d.polygon(outer,fill=m[0]);d.polygon(inner,fill=m[4]);d.line(edge,fill=m[5])
 d.rectangle((x-1,y-1,x+1,y+1),fill=c[1]);d.point((x,y),fill=c[4]);d.point((x,y-1),fill=c[5])
# Three independent hinges and a faceted spine clasp, all native-pixel detail.
for x,y in [(9,25),(13,37),(17,49)]:
 d.polygon([(x,y),(x+3,y-2),(x+5,y+2),(x+2,y+4)],fill=m[0])
 d.line([(x+1,y),(x+3,y-1),(x+4,y+2)],fill=m[4])
 d.point((x+1,y),fill=m[5])
d.polygon([(10,32),(14,28),(19,34),(15,40),(11,38)],fill=m[0])
d.polygon([(12,32),(14,30),(17,34),(15,38),(12,36)],fill=m[4])
d.polygon([(13,33),(14,32),(16,34),(14,36)],fill=c[3]);d.point((14,33),fill=c[5])
# Thin orbit: one clean line, differentiated satellites and an unmistakable star.
orbit=[(25,31),(26,27),(31,24),(39,24),(45,28),(46,32),(43,37),(35,40),(28,37),(25,31)]
d.line(orbit,fill=c[3]);d.line([(26,28),(28,26),(31,24),(37,24)],fill=c[4])
d.line([(28,18),(34,16),(43,19),(49,26),(50,32),(46,40),(40,44),(33,43)],fill=v[3])
d.line([(34,17),(40,19)],fill=v[1])
for x,y in [(34,16),(46,40)]:
 d.line([(x-2,y),(x+2,y)],fill=v[4]);d.line([(x,y-2),(x,y+2)],fill=v[4]);d.point((x,y),fill=v[5])
for x,y in [(25,31),(43,37)]:
 d.rectangle((x-1,y-1,x+1,y+1),fill=c[3]);d.point((x,y),fill=c[5])
d.polygon([(35,24),(37,29),(43,31),(37,33),(35,38),(33,33),(27,31),(33,29)],fill=c[3])
d.polygon([(35,26),(36,30),(41,31),(36,32),(35,36),(34,32),(30,31),(34,30)],fill=c[5])
d.rectangle((34,30,36,32),fill=v[5])
for x,y in [(22,23),(41,15),(30,43)]:
 d.point((x,y),fill=m[5]);d.point((x+1,y+1),fill=m[3])

assert im.mode=='RGBA' and im.size==(64,64)
assert all(im.getpixel((x,y))[3]==0 for x,y in [(x,0) for x in range(64)]+[(x,63) for x in range(64)]+[(0,y) for y in range(64)]+[(63,y) for y in range(64)])
assert len(im.getcolors())>=16
out=HERE/'hd64';(out/'textures/item').mkdir(parents=True,exist_ok=True);(out/'models/item').mkdir(parents=True,exist_ok=True)
im.save(out/'textures/item/concord_codex.png')
model={'parent':'minecraft:item/generated','textures':{'layer0':'zerog_tweaks:item/concord_codex'}}
(out/'models/item/concord_codex.json').write_text(json.dumps(model,indent=2)+'\n')
preview=Image.new('RGB',(950,620),'#20232d');p=ImageDraw.Draw(preview)
p.text((24,20),'CONCORD CODEX - NATIVE 64x64 HD REDRAW',fill='#dcecff')
large=im.resize((512,512),Image.Resampling.NEAREST);preview.paste(large,(20,60),large)
p.text((590,70),'Native 64x64',fill='#dcecff');preview.paste(im,(625,110),im)
p.text((590,220),'Inventory-size simulation',fill='#dcecff')
small=im.resize((32,32),Image.Resampling.NEAREST);preview.paste(small,(640,265),small)
p.text((590,330),'Detail view: 3x',fill='#dcecff')
detail=im.resize((192,192),Image.Resampling.NEAREST);preview.paste(detail,(590,365),detail)
p.text((24,590),'Actual source pixels - not an in-game capture.',fill='#b8c2dc')
preview.save(HERE/'hd64-preview.png')
manifest={'resolution':[64,64],'alpha_bounds':im.getbbox(),'source':'native64 redraw, not an upscale','runtime_emission':False,'files':[]}
for rel in ('textures/item/concord_codex.png','models/item/concord_codex.json'):
 manifest['files'].append({'path':'assets/zerog_tweaks/'+rel,'sha256':hashlib.sha256((out/rel).read_bytes()).hexdigest()})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Native64 PNG/model and validation manifest created; runtime assets untouched.')
