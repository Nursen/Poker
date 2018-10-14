from Poker import *

##    HIGH_CARD = 1
##    ONE_PAIR = 2
##    TWO_PAIR = 3
##    THREE_OF_A_KIND = 4
##    STRAIGHT = 5
##    FLUSH = 6
##    FULL_HOUSE = 7
##    FOUR_OF_A_KIND = 8
##    STRAIGHT_FLUSH = 9
##    ROYAL_FLUSH = 10

deck = Deck()
handsPrinted = 0
minRank = 1
while handsPrinted < 100:
    try:
        pokerHand = PokerHand(deck.takeCards(5))
        if(pokerHand.category.value >= minRank):
            print(pokerHand)
            handsPrinted +=1
    except ValueError:
        deck = Deck()
        pokerHand = PokerHand(deck.takeCards(5))
        if(pokerHand.category.value >= minRank):
            print(pokerHand)
            handsPrinted +=1
