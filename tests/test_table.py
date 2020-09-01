import pathsetup
from card import Card
from cardset import CardSet
from table import Table
import unittest

class TestTable(unittest.TestCase):
    def test_append(self):
        table = Table()
        h2 = Card('h2')
        h3 = Card('h3')
        h4 = Card('h4')
        h5 = Card('h5')
        group = CardSet([h2, h3, h4])
        table.add_cards(group)
        table.add_cards(CardSet(h5))
        comparison_table = Table([CardSet([h2, h3, h4]), CardSet(h5)])
        self.assertTrue(table == comparison_table)

    def test_contains(self):
        h2 = Card('h2')
        h3 = Card('h3')
        h4 = Card('h4')
        h5 = Card('h5')
        group1 = CardSet([h2, h3])
        group2 = CardSet([h4, h5])
        table = Table([group1, group2])
        self.assertTrue(table.contains(group2))
        self.assertFalse(table.contains(h2))

    def test_add_to_target(self):
        h2 = Card('h2')
        h3 = Card('h3')
        h4 = Card('h4')
        h5 = Card('h5')
        h6 = Card('h6')
        h7 = Card('h7')
        group1 = CardSet([h2, h3])
        group2 = CardSet([h4, h5])
        group3 = CardSet([h6, h7])
        table = Table([group1, group2])
        table.add_cards_to_target_cards(added_set = group3, target_set = group2)
        self.assertTrue(table == Table([group1, CardSet([h4, h5,h6, h7])]))

if __name__ == '__main__':
    unittest.main()