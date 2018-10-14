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

    def __lt__(self,other):
        return self.other < other.value

    def __str__(self):
        images = {
              'HIGH_CARD' : u'\uf460',
              'ONE_PAIR' : u'\uf350',
              'TWO_PAIR' : u'\uf350\uf350',
              'THREE_OF_A_KIND' : u'\u2618',
              'STRAIGHT' : u'\uf4cf',
              'FLUSH' : u'\uf6bd',
              'FULL_HOUSE' : u'\uf3e0',
              'FOUR_OF_A_KIND' : u'\uf340',
              'STRAIGHT_FLUSH' : u'\uf4cf\uf6bd',
              'ROYAL_FLUSH' : u'\uf451\uf6bd'
        }

        return images[self.name] + ' ' + self.name[0] + str.lower(self.name[1:].replace('_',' '))

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

    def score(self):
        """ score function to give an integer value to a hand, useful for
        identifying ties/ equivalent hands """
        return (self.category.value * 10**4 +
                self.categoryRank.getRankNumericalValue() * 10**2 +
                sum([r.getRankNumericalValue() for r in self.kicker])
                )

    def bestHand(self, cards):
        """ Given a list of 5 or more unique cards, returns an array of the 5 cards that
        will result in the highest ranking Poker Hand."""

        cardsByRank = defaultdict(list)
        cardsBySuit = defaultdict(list)

        for c in cards:
            cardsByRank[c.rank].append(c)
            cardsBySuit[c.suit].append(c)

        cardsInRank = { k : len(cardsByRank[k]) for k in cardsByRank.keys() }
        cardsInSuit = { k : len(cardsBySuit[k]) for k in cardsBySuit.keys() }

        mostCardsInASuit = max(cardsInSuit.values())
        mostCardsInARank = max(cardsInRank.values())
        numRanks = len(cardsByRank.keys())

        #Check to see if prereqs for Royal Flush or Straight Flush are met.
        # Requires 5 consecutive cards of one suit, thus requiring 5 different
        # ranks

        if (mostCardsInASuit >=5 and numRanks >=5):
            potentialSuits = [n for n in cardsInSuit.keys() if cardsPerSuit[n] >= 5]
            potentialHands = [self.getHighestConsecutiveHand(cardsBySuit[s]) for
                    s in potentialSuits if
                    self.getHighestConsecutiveHand(cardsBySuit[s]) is not None]
            if any(potentialHands):
                return max(potentialHands)

        def assembleHandWithNOfRank(n):
            hand = []
            potentialRanks = [r for r in cardsInRank.keys() if cardsInRank[r] >= n ]
            hand.extend(cardsByRank[max(potentialRanks)][:n])
            hand.extend(self.getBestNCards([c for c in cards if c not in
                hand],5-n))
            return hand;
        # Check to see if prereqs for 4 of a kind are met.
        # Requires 4 cards of the same rank

        if mostCardsInARank >=4:
            return assembleHandWithNOfRank(4);
        #Check to see if prereqs for Full House are met.
        # Requires at least one rank with 3+ cards and at least 2 ranks with 2+
        # cards.
        if (mostCardsInARank >= 3 and len ([ v for v in cardsInRank.values() if v
            >=2]) >=2):
            hand = []
            potentialRanksFor3 = [ r for r in cardsInRank.keys() if cardsInRank[r] >= 3]
            rankOf3 = max(potentialRanksFor3)
            hand.extend(cardsByRank[rankOf3][:3])
            potentialRanksFor2 = [r for r in cardsInRank.keys() if cardsInRank[r] >= 2 and r != rankOf3]
            rankOf2 = max(potentialRanksFor2)
            hand.extend(cardsByRank[rankOf2][:2])
            return hand



        # Check to see if prereqs for Flush are met.
        # Requires 5 cards of one Suit.
        if (mostCardsInASuit >= 5):
            potentialSuits = [s for s in cardsInSuit.keys() if cardsPerSuit[s]
                    >= 5]
            potentialHands = [getBestNCards(cardsBySuit[s], 5) for s in
                    potentialSuits]
            return max(potentialHands)

        # Check to see if prereqs for Straight are met.
        # Requires 5 cards of consecutive Rank, thus requiring 5 different
        # ranks.

        if (numRanks >= 5):
            hand  = self.getHighestConsecutiveHand(cards)
            if hand is not None:
                return hand

        # Check to see if prereqs for 3 of a Kind are met.
        # Requires a rank with 3 cards

        if (mostCardsInARank >=3):
            return assembleHandWithNOfRank(3)

        # Check to see if prereqs for 2 Pair are met
        # Requires 2 ranks with 2 cards

        if (mostCardsInARank >= 2 and len([n for n in cardsInRank.values() if
            n >= 2]) >= 2):
            potentialRanks = [r for r in cardsInRank.keys() if cardsInRank[r] >=
                    2]
            firstRank = max(potentialRanks)
            secondRank = max([r for r in potentialRanks if r != firstRank])
            hand = cardsByRank[firstRank][:2]
            hand.extend(cardsByRank[secondRank][:2])
            hand.extend(self.getBestNCards([c for c in cards if c not in
                hand],1))
            return hand

        # Only a one pair or a high card can be returned, which one is
        # determined by the max cards per rank.

        return assembleHandWithNOfRank(mostCardsInARank)

    def getBestNCards(self, cards, n):
        if len(cards) < n:
            raise ValueError(f'Must have at least {n} cards to choose {n} best cards.')
        cards.sort(reverse=True)
        return cards[:n]

    def getHighestConsecutiveHand(self, cards):
        """ Given a list of cards, returns the highest ranking set of 5 cards in
        descending order, or None if no set of 5 consecutive cards exists."""
        if (len(cards) < 5):
            return None
        cards.sort(reverse=True)
        hand = [cards[0]]
        cardsToCollect = 4

        for i in range(1,len(cards)):
            if cardsToCollect == 0:
                return hand
            if(cards[i].rank.getRankNumericalValue() ==
                    hand[-1].rank.getRankNumericalValue() - 1):
                hand.append(cards[i])
                cardsToCollect -= 1
            elif cards[i].rank == hand[-1].rank:
                pass
            else:
                hand = [cards[i]]
                cardsToCollect = 4

        if len(hand) == 5:
            return hand

        return None






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
                PokerHandCategory.ONE_PAIR,
                PokerHandCategory.FULL_HOUSE
                ]
        # For all hands in this category, the kicker is the sorted cards
        # remaining after all cards of the category rank have been removed.

        if (self.category in rankMostRepeatedCategories):
            kickerRanks = [c.rank for c in self.cards if c.rank !=
                    self.categoryRank]
            kickerRanks.sort(reverse=True)
            return kickerRanks

        # Two pairs is the only  remaining hand category. The kicker is the
        # lower ranking pair, followed by the remaining 1 unpaired card's rank.

        cardsInRank = defaultdict(int)
        for c in self.cards:
            cardsInRank[c.rank] += 1

        kickerRanks = [min([ k for k in cardsInRank.keys() if cardsInRank[k] == 2]),
                [k for k in cardsInRank.keys() if cardsInRank[k] == 1][0]]
        return kickerRanks

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

        return f'{self.category} ( {self.categoryRank} ) | kicker: {kickerString} | cards: {cardString}'


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
        for _ in range(self.standardShuffleAttempts):
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

