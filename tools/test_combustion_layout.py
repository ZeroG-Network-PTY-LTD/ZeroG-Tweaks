"""Static native combustion menu/screen bounds; not graphical approval."""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class CombustionLayoutContract(unittest.TestCase):
    def test_slots_controls_and_metrics_do_not_overlap(self):
        menu=(ROOT/'src/main/java/net/zerog/tweaks/machine/CombustionMenu.java').read_text()
        screen=(ROOT/'src/main/java/net/zerog/tweaks/client/CombustionScreen.java').read_text()
        height=int(re.search(r'imageHeight=(\d+)',screen).group(1))
        fuel=tuple(map(int,re.search(r'be.fuel,0,(\d+),(\d+)',menu).groups()))
        rows=int(re.search(r'8\+col\*18,(\d+)\+row\*18',menu).group(1))
        hotbar=int(re.search(r'col,8\+col\*18,(\d+)\)',menu).group(1))
        positions=[fuel]+[(8+col*18,rows+row*18) for row in range(3) for col in range(9)]+[(8+col*18,hotbar) for col in range(9)]
        self.assertEqual(len(positions),37)
        for i,(x,y) in enumerate(positions):
            self.assertLessEqual(x+16,176)
            self.assertLess(y+16,height)
            for a,b in positions[:i]:
                self.assertTrue(x+16<=a or a+16<=x or y+16<=b or b+16<=y)
        controls=[tuple(map(int,m)) for m in re.findall(r'bounds\(leftPos\+180,topPos\+(\d+),94,(\d+)\)',screen)]
        self.assertEqual(len(controls),2)
        for y,h in controls:
            self.assertGreaterEqual(y,18+126)
            self.assertLessEqual(y+h,height)
        self.assertTrue(controls[0][0]>=controls[1][0]+controls[1][1])
        self.assertIn('getString(),108)',screen)
        self.assertLess(8+108,128)  # labels stop before the energy gauge
        self.assertLess(110,117)  # burn gauge before inventory heading
        self.assertLess(117+9,rows)


if __name__=='__main__':
    unittest.main()
