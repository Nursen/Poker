from enum import Enum, unique
from functools import total_ordering
from random import shuffle
from collections import defaultdict

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

    def __lt__(self, other):
        return self.getRankNumericalValue() < other.getRankNumericalValue()

    def getRankNumericalValue(self):
        faceRankValues = {
            'J' : 11,
            'Q' : 12,
            'K' : 13,
            'A' : 14
        }

        try:
            intValue = int(self.value)
        except ValueError:
            intValue = faceRankValues[self.value]

        return intValue

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

    def initFromString(self, card):
        """ Initalize a card object from a string representation of the rankfollowed by the suit (Ex: 4H = 4 of Hearts)
        The suit is given by the first letter of the suit name. E.g Hearts: H, Clubs: C.
        Ranks for non-numeric cards are given by the first letter of the rank. E.g. Queen: Q, Ace: A
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
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self,other):
        return self.other < other.value

    def __str__(self):
        return str.lower(self.name.replace('_',' '))

@total_ordering
class PokerHand(object):
    def __init__(self, cards):
        if (cards == None or len(cards) < 5):
            raise TypeError('Must have at least 5 cards to make a Poker Hand')
        if (len(cards) == 5):
            self.cards = cards
            self.cards.sort(reverse=True)
            self.category = self.determineCategory()
            self.categoryRank = self.determineCategoryRank()
            self.kicker = self.determineKicker()
        else:
            self.cards = self.bestHand(cards)
            self.cards.sort(reverse = True)
            self.category = self.determineCategory()
            self.categoryRank = self.determineCategoryRank()
            self.kicker = self.determineKicker()

    def determineCategory(self):
        cardsByRank = defaultdict(list)
        cardsBySuit = defaultdict(list)

        for c in self.cards:
            cardsByRank[c.rank].append(c)
            cardsBySuit[c.suit].append(c)

        numRanks = len(cardsByRank.keys())
        numSuits = len(cardsBySuit.keys())

        rankCounts = list(map(lambda x: len(cardsByRank[x]),
            cardsByRank.keys()))
        rankCounts.sort(reverse=True)
        #TODO change diffRanks to isConsecutive
        diffRanks = self.cards[0].rank.getRankNumericalValue() - self.cards[len(self.cards) - 1].rank.getRankNumericalValue()


        # Check for Royal Flush and Straight
        # Prereqs: Cards are Consecutive and there is only one Suit
        # The Highest card is an Ace, it's a Royal Flush
        # The Highest card is not an Ace, it's a Straight Flush
        if (diffRanks == 4 and numSuits == 1):
            if (self.cards[0].rank == Rank.ACE):
                return PokerHandCategory.ROYAL_FLUSH
            else:
                return PokerHandCategory.STRAIGHT_FLUSH

        # Check for 4 of a Kind or Full House,
        # Prereqs: There are 2 Ranks.
        # The count of a rank is in [4, 1] it's a Four of a kind
        # The count of a rank is in [2, 3], it's a Full House
        if (numRanks == 2):
            if (rankCounts[0] == 4):
                return PokerHandCategory.FOUR_OF_A_KIND
            else:
                return PokerHandCategory.FULL_HOUSE

        # Check for a Straight or Flush
        # Prereqs: There are 5 Ranks
        # If there is one Suit, it's a Flush
        # If the cards are consecutive, it's a Straight
        if (numRanks == 5):
            if (numSuits == 1):
                return PokerHandCategory.FLUSH
            elif (diffRanks == 4):
                return PokerHandCategory.STRAIGHT

        # Check for 3 of A Kind or Two Pair
        # Prereqs: There are 3 Ranks
        # Counts are [3, 1, 1] it's a 3Kind
        # Counts are [2, 2, 1] it's a 2Pair
        if (numRanks == 3):
            if (rankCounts[0] == 3):
                return PokerHandCategory.THREE_OF_A_KIND
            else:
                return PokerHandCategory.TWO_PAIR

        # Check for One Pair or High Card
        # Prereqs: There are more than 3 ranks, and it is not a Straight
        # If there are 4 ranks, it's One Pair
        # If there are 5 ranks, it's High Card
        if (numRanks == 4):
            return PokerHandCategory.ONE_PAIR

        return PokerHandCategory.HIGH_CARD

    def determineCategoryRank(self):
        highCardCategories = [
                PokerHandCategory.ROYAL_FLUSH,
                PokerHandCategory.STRAIGHT_FLUSH,
                PokerHandCategory.FLUSH,
                PokerHandCategory.STRAIGHT,
                PokerHandCategory.HIGH_CARD
                ]

        rankMostRepeatedCategories = [
                PokerHandCategory.FOUR_OF_A_KIND,
                PokerHandCategory.FULL_HOUSE,
                PokerHandCategory.THREE_OF_A_KIND,
                PokerHandCategory.ONE_PAIR
                ]

        # For all of these categories, the category rank is determined by the highest card, which is the first card since self.cards is sorted
        if (self.category in highCardCategories):
            return self.cards[0].rank

        cardsInRank = defaultdict(int)
        for c in self.cards:
            cardsInRank[c.rank] += 1
        # For all of these categories, the category rank is determined by the rank with the most cards in the hand, which is unique.
        if (self.category in rankMostRepeatedCategories):
            return max(cardsInRank, key=cardsInRank.get)

        # The only remaining Category is Two of a Kind, where the category rank is determined by the higher rank between the two pairs
        return max(
                list(
                    filter(
                        lambda x: cardsInRank.get(x) == 2,
                        cardsInRank.keys()
                        )
                    )
                )

    def determineKicker(self):
        highCardCategories = [
                PokerHandCategory.ROYAL_FLUSH,
                PokerHandCategory.STRAIGHT_FLUSH,
                PokerHandCategory.FLUSH,
                PokerHandCategory.STRAIGHT,
                PokerHandCategory.HIGH_CARD
                ]

        # For all hands in this category, the kicker is the sorted hand without
        # the high card.
        if (self.category in highCardCategories):
            return list(map(lambda c: c.rank, self.cards[1:]))

        rankMostRepeatedCategories = [
                PokerHandCategory.FOUR_OF_A_KIND,
                PokerHandCategory.THREE_OF_A_KIND,
                PokerHandCategory.ONE_PAIR
                ]

        cardsInRank = defaultdict(int)
        for c in self.cards:
            cardsInRank[c.rank] += 1
        # For all hands in this category, the kicker is the sorted cards remaining
        # after all cards of the rank with the highest number of cards have been
        # removed.
        if (self.category in rankMostRepeatedCategories):
            kickerRanks = [c.rank for c in self.cards if c.rank !=
                    self.categoryRank]
            kickerRanks.sort(reverse=True)
            return kickerRanks
        # For the remaining hand categories, the tie-breaker is the rank with
        # the second-most cards. for 2Pair the rank will have 1 card, for Full
        # House the rank will have 2 cards.
        kickerCardCount = {
                PokerHandCategory.TWO_PAIR : 1,
                PokerHandCategory.FULL_HOUSE : 2
                }

        return list(filter(
            lambda x: cardsInRank[x] == kickerCardCount[self.category],
            cardsInRank.keys()))

    def __eq__(self, other):
        return (
                self.category == other.category and
                self.categoryRank == other.categoryRank and
                self.kicker == other.kicker
                )

    def __lt__(self, other):
        # Compare categories first
        if (self.category != other.category):
            return self.category < other.category
        # If categories are the same, compare the category highest rank
        if (self.categoryRank != other.categoryRank):
            return self.categoryRank < other.categoryRank
        # If the category highest ranks are the same, compare the first nonidentical kicker element
        if (self.kicker != other.kicker):
            for i in range(len(self.kicker)):
                if self.kicker[i] != other.kicker[i]:
                    return self.kicker[i] < other.kicker[i]
        # If the category and kicker are equal, the hands are equal, not less
        # than. Return false.
        return False

    def __str__(self):
        if (self.kicker is None):
            kickerString = 'N/A'
        else:
            kickerString = str.join(' ', [str(k) for k in self.kicker])

        cardString = str.join(' ', [str(c) for c in self.cards])

        return f'{self.category} ( {self.categoryRank} ) | kicker:{kickerString} | cards: {cardString}'


class Deck(object):
    """ A deck of cards supporting pulling cards from the top of the deck and
    shuffling the deck.
    If initialized without a set of cards, will generate and shuffle a standard
    52-card deck of cards to begin"""
    standardShuffleAttempts = 3

    def __init__ (self, cards = None):
        if (cards == None):
            self.cards = self.getStandardSortedDeck()
            self.shuffle()
        else:
            self.cards = cards

    def shuffle(self):
        for i in range(self.standardShuffleAttempts):
            shuffle(self.cards)

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

    def __str__(self):
        maxPerLine = len(self.cards) // 5
        return str.join('\n',
                [str.join(' ',
                    [str(c) for c in self.cards][i:i+maxPerLine]
                 ) for i in
                range(0, len(self.cards), maxPerLine)]
                )

