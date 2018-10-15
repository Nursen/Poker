Thank you for taking the time to look over my Poker Hand solution. For this
problem, I decided to forego my usual language of C# in favor of python, with I
think is more heavily used at the Broad. I modeled the cards myself, and tried
to make a package that could easily be used to implement other card games. I
include a Deck object in the package, which I used in some manual testing
throughout development, and also in the Simulation file. The PokerHandSimulation
file is included, feel free to run the functions with or without additional
parameters to generate Poker hands or run tournaments. To generate a simulated
tournament as a text file, run

python -c "import PokerHandSimulation; PokerHandSimulation.runPokerTournaments()" >> sampleResults.txt


To test the functions, you will need Python 3.6.
Run a python shell in the directory containing the unzipped files.
Import all functions from BroadPokerTests, then follow the solution instructions
for the problem you would like to test

For ease of testing, the method createSampleHands can be used to randomly generate a list
of inputs. Just pass in the number of samples you would like, and the number of
cards in each sample. Ex. hands = createSampleHands(50, 5) will return a list of
50 5-card lists in the standard representation for input as specified below.

#1. Write a function that takes a 5-card hand as a JSON array and determines its
category, with any tiebreaking information that is necessary. For example, the
input ["JH", "4C", "4S", "JC","9H"] would have the value of two pair: jacks and
4s with a 9 kicker. You may choose your own representation for the output.

SOLUTION EXAMPLE:
input = ["JH", "4C", "4S", "JC", "9H"]
whatsMyHand(input)

The solution will be printed on your screen, with the description of the hand,
the category rank, any kicker information, and a list of the cards.

#2. Write a function that takes 2 or more 5-card hands and determines the
winner.

SOLUTION EXAMPLE*:
inputs = createSampleHands(50,5)
input1 = inputs[4]
input2 = inputs[9]
input3 = inputs[40]

whoIsTheWinner(input1, input2, input3)
whoIsTheWinner(inputs)

The solution will be printed on your screen. For ties, all winners will be
printed on your screen.

*This function can take input in two forms (1) A list of 5-card lists (2) Two or
more lists of 5-card lists passed directly as arguments into the method call.
(Fun fact, you can also pass lists of more than 5 cards, the best hand out of
the cards passed in will be automatically chosen for that player's hand.)

#3. Some poker variations use more than 5 cards per player, and the
player chooses the best subset of 5 cards to play. Write a function that takes 5
or more cards and returns the best 5-card hand that can be made with those
cards. For example, the input ["3H", "7S", "3S", "QD", "AH", "3D", "4S"] should
return [3H, 3S, 3D, AH, QD], which is a 3-of-a-kind with 3s, ace and queen kickers.

SOLUTION EXAMPLE:
input = ["JH", "4C", "4S", "JC", "9H", "10C", "QS", "AD"]
whichCardsShouldIChoose(input)

The solution is returned as a string array in the same format as the input.

As a last note, please forgive my colorful interpretations of the types of hands
in Poker. I had to learn how Poker worked for this project, and couldn't resist
laughing at the naming of the hands, so I wanted to share the joke. ;)

You will find an exceedingly sparse list of tests, and a long list of TODOs in
the PokerTests.py file. 
