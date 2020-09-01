import pathsetup
from cardset import CardSet
from card import Card
import unittest

class TestCardSet(unittest.TestCase):
    def test_consecutive(self):
        s2 = Card('s2')
        s2.hidden_int_value = 5
        s2.hidden_suit = 'h'
        s2.hidden_rank = '5'
        h4 = Card('h4')
        h6 = Card('h6')

        # case 1
        group = CardSet([h4, s2, h6])
        self.assertTrue(group.consecutive)
        self.assertFalse(group.same_rank)
        self.assertTrue(group.wc_is_in_cards)

        # case 2 
        d2 = Card('d2')
        d2.hidden_suit = 'd'
        d2.hidden_int_value = 7
        d2.hidden_rank = '7'
        group = CardSet([h4, s2, h6, d2])
        self.assertTrue(group.consecutive)
        self.assertFalse(group.same_rank)

        # case 3
        group = CardSet([s2, h4, h6])
        self.assertFalse(group.consecutive)
        self.assertFalse(group.same_rank)
        self.assertTrue(group.wc_is_in_cards)

        # case 4
        d5 = Card('d5')
        c5 = Card('c5')
        group = CardSet([s2, d5, c5])
        self.assertFalse(group.consecutive)
        self.assertTrue(group.same_rank)
        self.assertTrue(group.wc_is_in_cards)

    def test_sort(self):
        s2 = Card('s2')
        s2.hidden_suit = 'h'
        s2.hidden_int_value = 5
        s2.hidden_rank = '5'
        h4 = Card('h4')
        h6 = Card('h6')
        d2 = Card('d2')
        d2 = Card('d2')
        d2.hidden_suit = 'd'
        d2.hidden_int_value = 7
        d2.hidden_rank = '7'
        group = CardSet([h4, s2, d2, h6])
        group.sort_cards()
        comparison_group = CardSet([h4, s2, h6, d2]) # what the cards should look like
        self.assertEqual(group.card_ids, comparison_group.card_ids)

    def test_isin(self):
        # case 1
        h3 = Card('h3')
        h4 = Card('h4')
        h5 = Card('h5')
        group = CardSet([h3, h4, h5])
        self.assertTrue(h3.isin(group))

        # case 2: wildcard
        c2 = Card('c2')
        c2.hidden_suit = 'H'
        c2.hidden_int_value = 3
        c2.hidden_rank = '3'
        self.assertTrue(c2.isin(group)) 
        self.assertTrue(c2 == h3) # c2 is considered to be in the group since c2 == h3 after assigning new attrs
        c2.reset_wildcard_attrs()
        self.assertFalse(c2.isin(group)) # c2 is no longer in the group after resetting its attributes
        self.assertFalse(c2 == h3)

    def test_append_extend(self):
        # case 1: appending a card object:
        h3 = Card('h3')
        group = CardSet(h3)
        h4 = Card('h4')
        group.append(h4)
        self.assertTrue(group == CardSet([h3, h4]))

        # case 2: appending a card_set object
        card_set = CardSet([h3, h4])
        group.extend(card_set)
        self.assertTrue(group == CardSet([h3, h3, h4, h4]))

    def test_remove(self):
        # case 1: removing a card object
        h3 = Card('h3')
        h4 = Card('h4')
        h5 = Card('h5')
        group = CardSet([h3, h4, h5])
        card2remove = h3
        group.remove(card2remove)
        self.assertTrue(group == CardSet([h4, h5]))
        self.assertFalse(group.contains(h3))
        self.assertFalse(h3.isin(group))

        # case 2: removing a card_set object
        group = CardSet([h3, h4, h5])
        to_remove = CardSet([h3, h4])
        group.remove(to_remove)
        self.assertTrue(group == CardSet(h5))

    def test_eq(self):
        h3 = Card('h3')
        group = CardSet(h3)
        self.assertFalse(h3 == group)

        h2 = Card('h2')
        h4 = Card('h4')
        h5 = Card('h5')
        h6 = Card('h6')

        h2.assign_wildcard_attrs() # assign 'h' and 4 as hidden attrs
        group1 = CardSet([h2, h5, h6])
        group2 = CardSet([h4, h5, h6])
        self.assertTrue(h2 == h4)
        self.assertTrue(group1 == group2)
        self.assertTrue(group1.contains(group2))

        group2.remove(h2) # since h2 and h4 are equal, removing h2 should in effect remove h4
        self.assertTrue(group2 == CardSet([h5, h6]))

        group2 = CardSet([h4, h5, h6])
        group2.remove(CardSet([h2, h5]))
        print(group2)
        self.assertTrue(group2 == CardSet([h6]))

    def test_contains(self):
        h3 = Card('h3')
        h4 = Card('h4')
        h5 = Card('h5')
        h6 = Card('h6')
        child_group = CardSet([h3, h4, h5])
        parent_group = CardSet([h3, h4, h5, h6])
        self.assertTrue(parent_group.contains(child_group))
        self.assertTrue(child_group.isin(parent_group))
        self.assertFalse(child_group.contains(parent_group))
        self.assertTrue(child_group.contains(h3))
        self.assertTrue(child_group.contains(CardSet(h3)))

if __name__ == '__main__':
    unittest.main()