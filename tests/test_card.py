import pathsetup
from card import Card
import unittest

class TestCards(unittest.TestCase):
    def test_adj_cards(self):
        ha = Card('ha')
        h2 = Card('h2')
        result1 = ha.adjacent(h2)
        result2 = h2.adjacent(ha)
        self.assertTrue(result1)
        self.assertTrue(result2)

    def test_btw_cards(self):
        ha = Card('ha')
        h2 = Card('h2')
        hk = Card('hk')
        true_result = ha.between(h2, hk)
        false_result = h2.between(ha, hk)
        self.assertTrue(true_result)
        self.assertFalse(false_result)

    def test_equals(self):
        h2_static = Card('h2')
        h2_change = Card('h2')
        h2_change.assign_wildcard_attrs()
        self.assertTrue(h2_static == h2_change)

if __name__ == '__main__':
    unittest.main()