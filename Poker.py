from enum import Enum, unique
from functools import total_ordering
from random import shuffle

@unique
class Suit(Enum):
    """ Suits of a Standard Deck of Cards """
    HEARTS = 'H'
    CLUBS = 'C'
    DIAMONDS = 'D'
    SPADES = 'S'

    def __str__(self):
        switcher = {
                'H' : u'\u2665',
                'C' : u'\u2663',
                'D' : u'\u2666',
                'S' : u'\u2660'
        }
        return switcher[self.value]

@total_ordering
@unique
class Rank(Enum):
    """ Ranks of a Standard Deck of Cards. Supports Comparison with Ace as high
    card only """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.getRankValue(self.value) == self.getRankValue(other.value)

    def __lt__(self, other):
        return self.getRankValue(self.value) < self.getRankValue(other.value)

    def getRankValue(self, value):
        faceRankValues = {
            'J' : 11,
            'Q' : 12,
            'K' : 13,
            'A' : 14
        }

        try:
            trueValue = int(value)
        except ValueError:
            trueValue = faceRankValues[value]

        return trueValue

@total_ordering
class Card (object):
    """ Card Object with a Rank and Suit. Supports Comparison by Rank """
    def __init__ (self, *args, **kwargs):
        if (len(args) == 1 and isinstance(args[0], str)):
            try:
                self.initFromString(args[0])
            except:
                raise
        elif (len(args) == 2 and isinstance(args[0], Rank) and
                isinstance(args[1], Suit)):
                self.suit = args[1]
                self.rank = args[0]
        else:
            raise TypeError

    def initializeFromString(self, card):
        """ Initalize a card object from a string representation of the rankfollowed by the suit (Ex: 4H = 4 of Hearts)
        The suit is given by the first letter of the suit name. E.g Hearts: H, Clubs: C. 
        Ranks for non-numeric cards are
        given by the first letter of the rank. E.g. Queen: Q, Ace: A 
        Raises a ValueError if invalid Suit or Rank is supplied."""

        suitStr = card[-1]
        try:
            self.suit = Suit(suitStr)
        except ValueError:
            raise

        rankStr = card[:-1]
        try:
            self.rank = Rank(int(rankStr))
        except ValueError:
            try:
                self.rank = Rank(rankStr)
            except:
                raise

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

@total_ordering
@unique
class PokerHandCategory(Enum):
    HIGH_CARD : 1
    ONE_PAIR : 2
    TWO_PAIR: 3
    THREE_OF_A_KIND: 4
    STRAIGHT: 5
    FLUSH: 6
    FULL_HOUSE: 7
    FOUR_OF_A_KIND: 8
    STRAIGHT_FLUSH: 9
    ROYAL_FLUSH: 10

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self,other):
        return self.other < other.value

    def __str__(self):
        return str.lower(self.name.replace('_',' '))

class Deck(object):
    """ A deck of cards supporting pulling cards from the top of the deck and
    shuffling the deck.
    If initialized without a set of cards, will generate and shuffle a standard
    52-card deck of cards to begin"""
    standardShuffleAttempts = 3

    def __init__ (self, cards = None):
        if (cards == None):
            self.cards = self.getStandardSortedDeck()
            #extra shuffling for fun and nostalgia
            for i in range(self.standardShuffleAttempts):
                shuffle(self.cards)
        else:
            self.cards = cards

    def takeCards(self, numCards=1):
        """Returns the top card in the deck and removes it from the Deck"""
        if (numCards < 1):
            raise ValueError('At least 1 card must be drawn from deck')
        if (len(self.cards) < numCards):
            raise ValueError('Not enough cards to draw from this deck.')
        drawnCards = self.cards[-numCards:]
        del self.cards[-numCards:]
        return drawnCards

    @classmethod
    def getStandardSortedDeck(cls):
        cards = []
        for s in Suit:
            for r in Rank:
                cards.append(Card(r,s))
        return cards



