"""Bounded source display dimensions, not a client lighting/render test."""
import re,unittest
from pathlib import Path
SOURCE=(Path(__file__).resolve().parents[1]/'src/main/java/net/zerog/tweaks/client/CompressorRenderer.java').read_text()
DIE=tuple(map(float,re.search(r'item\(be.displayDie,.*?overlay,([\d.]+)F,([\d.]+)F,([\d.]+)F,false\)',SOURCE).groups()))
RAM=tuple(map(float,re.search(r'\.20F,([\d.]+)F-([\d.]+)F\*compression',SOURCE).groups()))
SHAFT=tuple(map(float,re.search(r'\.44F,([\d.]+)F-([\d.]+)F\*compression',SOURCE).groups()))

class PressClearance(unittest.TestCase):
    def test_die_fills_bed_without_intersecting_chassis(self):
        y,scale,_=DIE
        width=12/16*scale
        self.assertGreaterEqual(width,.59)
        self.assertLess(width,10/16)
        bottom=y+(6/16-.5)*scale
        top=y+(9/16-.5)*scale
        self.assertGreater(bottom,3.5/16)
        self.assertLess(top,RAM[0]-RAM[1])
        self.assertIn('ItemDisplayContext.NONE',SOURCE)
    def test_ram_shaft_and_die_separated_through_cycle(self):
        for sample in range(101):
            compression=sample/100
            ram=RAM[0]-RAM[1]*compression
            shaft=SHAFT[0]-SHAFT[1]*compression
            self.assertAlmostEqual(ram+.10,shaft)
            self.assertLessEqual(shaft+.20+.25*compression,1)
            self.assertGreater(ram,.375)
if __name__=='__main__':unittest.main()
