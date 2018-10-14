import unittest
from Poker import *

##TODO Test Rank Comparison, esp face ranks
##TODO Test Card Comparison esp face cards
##TODO Test Card Construction from strings
##TODO Test Card Construction from Suit and Rank
##TODO Test Card Sorting, equality, inequality
##TODO Verify standard sorted deck contains every card
##TODO Verify Deck construction
##TODO Verify Deck takeCard removes correct cards. Confirm state before and after.
##TODO Verify comparison between PokerHandCategories
##TODO Verify comparison within PokerHandCatagories
##TODO Verify PokerHand constructor
##TODO Verify PokerHand comparison with different and same categories, category
## ranks, and kickers
##TODO Verify determineCategory method for PokerHand
##TODO Verify determineCategoryRank for PokerHand
##TODO Verify determineKicker for PokerHand
##TODO Verify best hand is selected in bestHand##
##TODO Verify helper methods used to get consecutive cards and highest rank
##cards

class TestPokerMethods(unittest.TestCase):

    def test_CompareStraightAnd3Kind_GetMax_ReturnsStraight(self):
        flush = ['6C', '5D', '4H', '3C', '2D']
        three_kind = ['KD', 'KS', 'KC', '10D', '2H']
        flushHand = getPokerHand(flush)
        three_kindHand = getPokerHand(three_kind)

        actual = max(flushHand, three_kindHand)
        expected = flushHand

        self.assertEqual(actual, expected)


def getPokerHand(hand):
    return PokerHand([Card(c) for c in hand])

if __name__ == '__main__':
    unittest.main()
