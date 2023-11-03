import random

class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = self.initialize_shoe()
        self.cut_card_position = self.get_cut_card_position()
        self.shuffle_shoe()

    def initialize_shoe(self):
        """Initialize multiple decks of cards into the shoe."""
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = values * 4  # One deck
        return deck * self.num_decks  # Multiple decks

    def shuffle_shoe(self):
        """Shuffle the decks in the shoe."""
        random.shuffle(self.cards)
        self.cut_card_position = self.get_cut_card_position()

    def get_cut_card_position(self):
        """Determine the cut card position for shuffling."""
        # This is typically 1/4 to 1/2 from the back of the shoe
        cut_position_min = int(len(self.cards) * 0.25)
        cut_position_max = int(len(self.cards) * 0.50)
        return random.randint(cut_position_min, cut_position_max)

    def deal(self):
        """Deal one card from the shoe."""
        if len(self.cards) == 0:
            raise ValueError("The shoe is out of cards; it must be shuffled before dealing.")
        return self.cards.pop(0)

    def shuffle_if_cut(self):
        """Determine if the cut card has been reached and shuffle if necessary."""
        if len(self.cards) <= self.cut_card_position:
            self.shuffle_shoe()
            return True
        return False
