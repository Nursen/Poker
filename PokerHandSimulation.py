from Poker import *
from BroadPokerTests import *
from string import Template

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

def generatePokerHands(minRank = 1, cardsToDraw = 5, handsToGenerate = 100):
    deck = Deck()
    handsPrinted = 0
    while handsPrinted < handsToGenerate:
        try:
            pokerHand = PokerHand(deck.takeCards(cardsToDraw))
            if(pokerHand.category.value >= minRank):
                print(pokerHand)
                handsPrinted +=1
        except ValueError:
            deck = Deck()
            pokerHand = PokerHand(deck.takeCards(cardsToDraw))
            if(pokerHand.category.value >= minRank):
                print(pokerHand)
                handsPrinted +=1

def runPokerTournaments(tournaments = 10, players = 5, cardsToDraw = 7):
    playerHands = createSampleHands(tournaments * players, 7)
    for i in range(tournaments):
        roundHands = playerHands[i * players : i * players + players]
        roundPlayers = { 'Player' + str(j+1) : roundHands[j] for j in
                range(players) }
        playerTemp = Template('$player | $hand')
        print (f'Round {i} : The players are : \n' +
                str.join('\n',[playerTemp.substitute(player = p, hand =
                    roundPlayers[p]) for p in roundPlayers.keys()]))
        whoIsTheWinner(playerHands[i*players:i*players + players])
