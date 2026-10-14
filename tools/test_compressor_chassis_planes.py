"""Reject same-facing overlapping coplanar chassis surfaces (trim z-fighting)."""
import itertools,json,unittest
from pathlib import Path

class ChassisPlanes(unittest.TestCase):
    def test_visible_planes_are_separated(self):
        path=Path(__file__).resolve().parents[1]/'src/main/resources/assets/zerog_tweaks/models/block/industrial_compressor.json'
        elements=json.loads(path.read_text())['elements']
        for i,j in itertools.combinations(range(len(elements)),2):
            a,b=elements[i],elements[j]
            for axis in range(3):
                for edge in ('from','to'):
                    if a[edge][axis]!=b[edge][axis]:continue
                    overlap=all(min(a['to'][k],b['to'][k])>max(a['from'][k],b['from'][k]) for k in range(3) if k!=axis)
                    self.assertFalse(overlap,f'Coplanar faces: elements{i}/{j},axis{axis},{edge}')
if __name__=='__main__':unittest.main()
