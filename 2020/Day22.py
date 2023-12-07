from collections import deque
import copy, pickle
players = []

with open("Day22_input.txt") as f:
    lines = f.read().splitlines()
    count = -1
    for line in lines:
        if line.startswith('Player'):
            deck = []
            count += 1
            players.append(deck)
        elif line:
            players[count].append(int(line))

players_orig = copy.deepcopy(players)

# Play the cards
while min([len(deck) for deck in players]) > 0:
    # Get the highest card in each deck
    round = [deck.pop(0) for deck in players]
    # Which player has the highest card?
    winner = round.index(max(round))
    # Give the winning cards back to the winner, sorted by size. Highest first.
    players[winner].extend(list(reversed(sorted(round))))

# Winner!
counts = [len(deck) for deck in players]
winner = counts.index(max(counts))
winning_deck = players[winner]
mult = 1
total = 0
for card in reversed(winning_deck):
    total += mult*card
    mult += 1
print("Part 1:", total)

players = copy.deepcopy(players_orig)

def print_decks(cards, round, game):
    print("-- Round {} (Game {}) --".format(round, game))
    for i,p in enumerate(cards):
        print("Player {}'s deck: {}".format(i+1, ', '.join(['{}'.format(x) for x in p])))
              
def play(cards, game):
    # Check for the same condition in previous days
    previous_rounds = set()
    #turn = 1
    #print("\n== Game {} ==\n".format(game))

    # Play until one player has run out of cards
    while all([len(deck) > 0 for deck in cards]):
        #print_decks(cards,turn,game)

        # Get the first card in each deck
        round = [deck.pop(0) for deck in cards]
        
        #for i,c in enumerate(round):
        #    print("Player {} plays: {}".format(i+1,c))            
        # If every player has at least as many cards as the values just drawn then play a sub-game
        if all([len(deck) >= round[i] for i,deck in enumerate(cards)]):
            # Sub-game!
            #print("Playing a sub-game to determine the winner...")
            # Only use the number of cards on the current card from each player
            new_cards = [cards[i][:c] for i,c in enumerate(round)]
            winner = play(new_cards, game+1)
        else: # otherwise choose the winner
            # Which player has the highest card?
            winner = round.index(max(round))
            #print("Player {} wins round {} of game {}!\n".format(winner+1, turn, game))
            
        # Give the winning cards back to the winner, sorted by value. Highest first.
        cards[winner].append(round.pop(winner))
        cards[winner].extend(round)

        # If the new card config matches a previous config then player 1 wins!
        # Set comparisons are way faster than list comparisons. Pickle the cards to make a unique string to compare.
        if pickle.dumps(cards) in previous_rounds:
            # Player 1 wins!
            return 0
        else: # Add the current cards to the list
            previous_rounds.add(pickle.dumps(cards))

        #turn += 1

    # Game finished
    counts = [len(deck) for deck in cards]
    winner = counts.index(max(counts))
    #print("The winner of Game {} is Player {}!\n".format(game, winner+1))
    #print("Anyway, back to game {}...\n".format(game-1))
    return winner

play(players, 1)

# Winner!
counts = [len(deck) for deck in players]
winner = counts.index(max(counts))
winning_deck = players[winner]
mult = 1
total = 0
for card in reversed(winning_deck):
    total += mult*card
    mult += 1
print("Part 2:", total)

