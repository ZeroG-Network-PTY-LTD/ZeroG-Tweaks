"""Read-only component contract: metal whitelist, models, names, tags and native art.

Use --jar after the normal build to check the exact deliverable. No runtime
manufacturing recipes are assumed; their costs and machine route are pending.
"""
import argparse
import io
import json
from pathlib import Path
import re
import unittest
from zipfile import ZipFile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
EXPECTED=set('moonsteel lunarium ferrox olympium aresium cobaltium cyrrium aurelion azurium ruskite tectium pyrium basaltine salvium wraithsteel palladine rime_nickel photium radiantine astrium helion'.split())
JAR=None

class Components(unittest.TestCase):
    def test_only_dimension_metals(self):
        java=(ROOT/'src/main/java/net/zerog/tweaks/registry/ZGManufacturingComponents.java').read_text()
        metals=set(re.findall(r'"([a-z_]+)"',java.split('public static void init')[0]))
        self.assertEqual(metals,EXPECTED)
        self.assertNotIn('nullifite',metals)
        extra=json.loads((ROOT/'tools/planet_material_art_manifest.json').read_text())
        self.assertFalse(metals & {m['id'] for m in extra if m['gem']})
        init=(ROOT/'src/main/java/net/zerog/tweaks/registry/ModInit.java').read_text()
        self.assertLess(init.index('ZGManufacturingComponents.init()'),init.index('ItemInit.register'))

    def test_all_art_names_tags_and_jar(self):
        lang=json.loads((RES/'assets/zerog_tweaks/lang/en_us.json').read_text())
        jar=ZipFile(JAR) if JAR else None
        try:
            for kind,tag in [('cog','cogs'),('plate','plates')]:
                group=json.loads((RES/f'data/zerog_tweaks/tags/item/manufacturing/{tag}.json').read_text())['values']
                self.assertEqual(set(group),{f'zerog_tweaks:{metal}_{kind}' for metal in EXPECTED})
                for metal in EXPECTED:
                    identifier=f'{metal}_{kind}'
                    modelpath=f'assets/zerog_tweaks/models/item/{identifier}.json'
                    texpath=f'assets/zerog_tweaks/textures/item/manufacturing/{identifier}.png'
                    model=json.loads((RES/modelpath).read_text())
                    self.assertEqual(model['parent'],'minecraft:item/generated')
                    self.assertEqual(model['textures']['layer0'],f'zerog_tweaks:item/manufacturing/{identifier}')
                    self.assertIn(f'item.zerog_tweaks.{identifier}',lang)
                    im=Image.open(io.BytesIO((RES/texpath).read_bytes())).convert('RGBA')
                    self.assertEqual(im.size,(32,32))
                    x0,y0,x1,y1=im.getbbox()
                    self.assertTrue(1<=x0<x1<=31 and 1<=y0<y1<=31)
                    self.assertGreaterEqual(len(set(im.getdata())),6)
                    self.assertEqual(im.getpixel((0,0))[3],0)
                    if jar:
                        self.assertEqual(jar.read(modelpath),(RES/modelpath).read_bytes())
                        self.assertEqual(jar.read(texpath),(RES/texpath).read_bytes())
            if jar:
                self.assertIn('net/zerog/tweaks/registry/ZGManufacturingComponents.class',jar.namelist())
                self.assertFalse(any('gametest' in path.lower() for path in jar.namelist() if path.endswith('.class')))
        finally:
            if jar:jar.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);args=p.parse_args();JAR=args.jar
    unittest.main(argv=['manufacturing-components'],verbosity=2)
