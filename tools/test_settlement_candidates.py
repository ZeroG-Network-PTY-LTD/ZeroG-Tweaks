import unittest
from audit_settlement_candidates import candidate, search_candidates


class CandidateTests(unittest.TestCase):
    def test_verified_seed_zero_moon(self):
        self.assertEqual(candidate(0,'moon',0,1),(24,70))

    def test_verified_seed_zero_other_planets(self):
        self.assertEqual(candidate(0,'cerulon',0,1),(32,77))
        self.assertEqual(candidate(0,'eidolon',0,1),(22,67))
        self.assertEqual(candidate(0,'solvane',0,1),(18,83))

    def test_spacing_negative_regions_and_repeatability(self):
        for seed in (0,17,-323417769491979004):
            for rx in range(-2,3):
                for rz in range(-2,3):
                    x,z=candidate(seed,'moon',rx,rz)
                    self.assertTrue(rx*50+16<=x<=rx*50+33)
                    self.assertTrue(rz*50+16<=z<=rz*50+33)
                    self.assertEqual((x,z),candidate(seed,'moon',rx,rz))

    def test_search_is_bounded_unique_and_retains_original(self):
        for seed in (0,17,-323417769491979004):
            for rx in range(-2,3):
                for rz in range(-2,3):
                    sites=search_candidates(seed,'moon',rx,rz)
                    self.assertEqual(sites[0],candidate(seed,'moon',rx,rz))
                    self.assertEqual(len(sites),len(set(sites)))
                    self.assertTrue(3<=len(sites)<=5)
                    for x,z in sites:
                        self.assertTrue(rx*50+16<=x<=rx*50+33)
                        self.assertTrue(rz*50+16<=z<=rz*50+33)


if __name__ == '__main__':
    unittest.main()
