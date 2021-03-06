from Poker import *
from string import Template

def whatsMyHand(cardArray):
    hand = PokerHand([Card(c) for c in cardArray])
    print(hand)

def whoIsTheWinner(*args, **kwargs):
    if len(args) == 1:
            args = [item for sublist in args for item in sublist]

    players = dict()
    for i in range(len(args)):
        players['Player' + str(i+1)] = PokerHand([Card(c) for c in args[i]])
    bestHand = max(players.values())
    winners = [p for p in players.keys() if players[p].score() ==
            bestHand.score()]

    if len(winners) == 1:
        print(f'The winner of this showdown is {winners[0]}:\n{bestHand}')
    else:
        winnerTemp = Template('$player\n$hand')
        print(f'We have a {len(winners)}-way tie! The winners are:' + 
                str.join('\n',[winnerTemp.substitute(player = p, hand = str(players[p])) for p
            in winners]))

def whichCardsShouldIChoose(cards):
    hand = PokerHand([Card(c) for c in cards])
    return [str(c.rank.value) + str(c.suit.value) for c in hand.cards]

def createSampleHands(N,C):
    """ returns a list of N lists of string representations of C cards drawn
    randomly from a deck. C must be less than or equal to 52, as that is the number of cards in a deck. """
    if (C > 52):
        raise ValueError("Number of cards must be less than or equal to 52")
    deck = Deck()
    handsInDeck = 0
    hands = []
    while handsInDeck < N:
        try:
            hands.append(cardListString(deck.takeCards(C)))
            handsInDeck += 1
        except ValueError:
            deck = Deck()
    return hands

def cardListString(cards):
    return [str(c.rank.value) + str(c.suit.value) for c in cards]

