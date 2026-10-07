"""Deterministic graph contracts; does not start Minecraft or claim worldgen proof."""
import unittest
from audit_structure_routes import trace


class RouteTests(unittest.TestCase):
    def test_cycles_fallbacks_and_nested_lists_are_bounded(self):
        pools = {'test:start': {'fallback': 'test:fallback', 'elements': [{'weight': 1, 'element': {
            'element_type': 'minecraft:list_pool_element', 'elements': [
                {'element_type': 'minecraft:single_pool_element', 'location': 'test:room'}]}}]},
            'test:fallback': {'fallback': 'test:start', 'elements': []}}
        result = trace('test:start', pools, {'test:room': {'outgoing_pools': ['test:start']}})
        self.assertEqual(result['potential_templates'], ['test:room'])
        self.assertEqual(result['missing_references'], [])
        self.assertEqual(len(result['potential_pools']), 2)

    def test_missing_template_and_connector_pool_remain_visible(self):
        pools = {'test:start': {'elements': [
            {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'test:gone'}},
            {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'test:room'}}]}}
        result = trace('test:start', pools, {'test:room': {'outgoing_pools': ['test:gone_pool']}})
        self.assertEqual(result['missing_references'], ['test:gone', 'test:gone_pool'])

    def test_zero_weight_and_feature_elements_do_not_fabricate_template_routes(self):
        pools = {'test:start': {'elements': [
            {'weight': 0, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'test:dead'}},
            {'weight': 1, 'element': {'element_type': 'minecraft:feature_pool_element', 'feature': 'test:plant'}}]}}
        result = trace('test:start', pools, {})
        self.assertEqual(result['potential_templates'], [])
        self.assertEqual(result['non_template_elements'], ['minecraft:feature_pool_element'])


if __name__ == '__main__':
    unittest.main()
