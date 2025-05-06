# Tricksy Battle Game
# A simple 2-player trick-taking card game implemented in the terminal
# Players alternate leading and following cards; highest card in the lead suit wins each trick


import random

class Card:
    # Represents a single playing card with suit and rank
    # Provides a numeric value for comparison based on rank
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'Ace']
    # Map '2'->2 through 'Ace'->14
    VALUE_MAP = {rank: i+2 for i, rank in enumerate(RANKS)}

    def __init__(self, suit, rank):
        # Initialize card with given suit and rank, set its numeric value
        self.suit = suit
        self.rank = rank
        self.value = Card.VALUE_MAP[rank]

    def __str__(self):
        # Human-readable representation, e.g., "Queen of Hearts"
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        # Debug representation matches str()
        return str(self)
    
class Deck:
    # Represents a 48-card deck (Kings removed)
    # Supports shuffling, dealing, and drawing
    def __init__(self):
        # Create and shuffle the deck
        self.cards = [Card(s, r) for s in Card.SUITS for r in Card.RANKS]
        random.shuffle(self.cards)

    def deal(self, n):
        # Deal n cards from the top of the deck
        return [self.cards.pop() for _ in range(n)]
    
    def draw(self):
        # Reveal one card (pop from deck) or None if empty
        return self.cards.pop() if self.cards else None
    
class Player:
    # Represents a game player with a name and hand of cards
    def __init__(self, name):
        self.name = name
        # List of cards objects
        self.hand = []

def prompt_card_choice(player, valid_choices):
    # Prompt the given player to select one card from valid_choices
    # Prints indexed list, reads input, and returns the chosen card
    while True:
        # Display choices with indices
        for idx, card in enumerate(valid_choices, 1):
            print(f"    {idx}: {card}")
        choice = input(f"{player.name}, choose a card (1-{len(valid_choices)}): ")
        if choice.isdigit():
            i = int(choice) - 1
            # Validate the index range
            if 0 <= i < len(valid_choices):
                return valid_choices[i]
        print("Invalid selection; try again.")

def get_lead_card(player):
    # Let the leader pick any card from their hand to lead the trick
    print(f"\n{player.name}'s hand: " + ", ".join(str(c) for c in player.hand))
    return prompt_card_choice(player, player.hand)

def get_follow_card(player, lead_suit):
    # Force the follower to follow suit if possible; otherwise allow any card
    # Filter cards matching the lead suit
    same_suit = [c for c in player.hand if c.suit == lead_suit]
    if same_suit:
        print(f"{player.name}, you must follow suit ({lead_suit}):")
        return prompt_card_choice(player, same_suit)
    else:
        print(f"{player.name}, you have no {lead_suit}. Play any card: ")
        return prompt_card_choice(player, player.hand)

def determine_winner(lead_player, lead_card, follow_player, follow_card):
    # Determine the winner of the trick:
    # If follower followed suit, compare value
    # Otherwise, leader wins by default
    if follow_card.suit == lead_card.suit:
        # Higher value wins among same suit
        return follow_player if follow_card.value > lead_card.value else lead_player
    else:
        # Failure to follow suit gives the leader the trick
        return lead_player
    
def early_termination(score1, score2):
    # Check for early end: one player reachers 9+ points while opponent has ≥ 1
    return (score1 >= 9 and score2 >= 1) or (score2 >= 9 and score1 >= 1)

def main():
    # Game setup
    print("Welcome to Tricksy Battle!\n")
    p1 = Player(input("Enter name for Player 1: ").strip() or "Player 1")
    p2 = Player(input("Enter name for Player 2: ").strip() or "Player 2")

    deck = Deck()
    # Deal 8 cards to each player
    p1.hand = deck.deal(8)
    p2.hand = deck.deal(8)

    score = {p1.name: 0, p2.name: 0}

    # Randomly choose initial leader
    leader, follower = (p1, p2) if random.choice([True, False]) else (p2, p1)
    print(f"\n{leader.name} will lead the first trick.\n")

    # Track extra deals when hands drop to 4 twice
    deals_done = 0
    round_num = 0

    # Main game loop: up to 16 rounds or early termination
    while round_num < 16 and not early_termination(score[p1.name], score[p2.name]):
        round_num += 1
        print(f"--- Round {round_num} ---")

        # Leader plays
        lead_card = get_lead_card(leader)
        leader.hand.remove(lead_card)
        print(f"{leader.name} leads: {lead_card}")

        # Follower plays
        follow_card = get_follow_card(follower, lead_card.suit)
        follower.hand.remove(follow_card)
        print(f"{follower.name} plays: {follow_card}")

        # Determine trick winner and update score
        winner = determine_winner(leader, lead_card, follower, follow_card)
        print(f"{winner.name} wins the trick!\n")
        score[winner.name] += 1

        # Next leader is trick winner
        leader, follower = (winner, p1 if winner is p2 else p2)

        # Reveal one card from deck each trick
        rev = deck.draw()
        if rev: 
            print(f"Revealed from deck: {rev}")

        # Deal additional cards when hands drop to 4 (twice)
        if len(p1.hand) == 4 and len(p2.hand) == 4 and deals_done < 2:
            print("\nDealing 4 new cards to each player...\n")
            p1.hand.extend(deck.deal(4))
            p2.hand.extend(deck.deal(4))
            deals_done += 1

        # Show current score
        print(f"Score → {p1.name}: {score[p1.name]} | {p2.name}: {score[p2.name]}\n")

    # Game end summary
    print("=== GAME OVER ===")
    print(f"Final Score → {p1.name}: {score[p1.name]} | {p2.name}: {score[p2.name]}")
    # Handle "shoot the moon" scenario
    if score[p1.name] == 0 and score[p2.name] == 16:
        print(f"{p1.name} shot the moon and wins 17-{score[p2.name]}!")
    elif score[p2.name] == 0 and score[p1.name] == 16:
        print(f"{p2.name} shot the moon and wins 17-{score[p1.name]}!")
    elif score[p1.name] > score[p2.name]:
        print(f"{p1.name} wins!")
    elif score[p2.name] > score[p1.name]:
        print(f"{p2.name} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
