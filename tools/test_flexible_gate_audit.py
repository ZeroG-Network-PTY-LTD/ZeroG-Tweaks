"""Pure snapshot tests; no Minecraft client, saves or network touched."""
import unittest
from audit_saved_gate_layout import resolve_layout, rotate, SIDES
from generate_gate_build_guide import parts


class FlexibleAuditTests(unittest.TestCase):
    def test_all_tiers_directions_and_controller_sides(self):
        checked=0
        for tier in range(1,7):
            for facing in SIDES:
                for side in SIDES:
                    blocks={rotate(p,facing):{'Name':'zerog_tweaks:'+b} for p,b in parts(tier).items()
                            if b not in {'gate_controller','gate_energy_port'}}
                    controller=rotate((0,1,-tier-1),side)
                    visual=SIDES[(SIDES.index(side)+1)%4]
                    blocks[controller]={'Name':'zerog_tweaks:gate_controller'}
                    required=4 if tier>=5 else 2 if tier>=3 else 1
                    port_side=SIDES[(SIDES.index(side)+1)%4]
                    for x in (-1,1,-2,2)[:required]:blocks[rotate((x,1,-tier-1),port_side)]={'Name':'zerog_tweaks:gate_energy_port'}
                    state=lambda p:blocks.get(p,{'Name':'minecraft:air'})
                    result=resolve_layout(state,controller,visual,[(controller,visual)])
                    self.assertEqual(result['formed_tier'],tier,(tier,facing,side,result))
                    self.assertEqual(result['centre'],(0,0,0));checked+=1
        self.assertEqual(checked,96)


if __name__=='__main__':unittest.main()
