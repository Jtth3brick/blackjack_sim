from strat import strat
from hand import Hand

NUM_CARDS_IN_DECK = 52

class BasicPlayer:
    """
    Represents a player playing basic strategy in a game of Blackjack.
    """
    def __init__(self, gamestate):
        self.hands = []
        self.gamestate = gamestate
        self.bet_amount = 1
    
    def get_balance(self):
        return self.gamestate.get_player_balance()

    def new_round(self):
        """
        Prepares the player for a new round.

        :param player_balance: The current balance of the player
        :return: The bet amount for the new round
        """
        return self.bet_amount

    def set_hands(self, hands):
        """
        Sets the player's hands for the round.

        :param hands: A list of Hand instances
        """
        self.hands = hands

    def play(self):
        """
        The main decision loop for the player's game actions.
        """
        for hand in self.hands:
            if (not hand.is_complete()) and hand.get_value() >= 21:
                hand.set_complete()
                hand.set_decision('stand')
            if not hand.is_complete():
                decision = strat(hand)
                hand.set_decision(decision)
                if decision == 'stand' or decision == 'surrender' or decision == 'double':
                    hand.set_complete()

    def get_bet(self, hand):
        """
        Retrieves the bet from the player for the round.

        :return: The bet amount
        """
        return self.new_round()
    
    def play_more(self):
        return self.get_balance() >= 100

    def new_shoe(self):
        # Notifies player that a the shoe has been shuffled
        pass

    def update_count(self, card):
        """
        Update the count based on the value of the card.
        This method needs to be implemented based on the counting system being used.
        """
        pass

class BasicCounter(BasicPlayer):
    """
    Represents a player using a card counting system in addition to basic strategy in a game of Blackjack.
    """
    def __init__(self, gamestate):
        super().__init__(gamestate)
        self.count = 0  # Initialize the count
        self.num_cards_played = 0
        self.dec_count = ['10', 'J', 'Q', 'K', 'A']
        self.inc_count = ['2', '3', '4', '5', '6']
        self.no_count_change = ['7', '8', '9']
        self.num_decks = gamestate.shoe.num_decks
        assert type(self.num_decks) == int


    def play(self):
        """
        The main decision loop for the player's game actions, now incorporating card counting.
        Checks if a deviation from basic strategy is warranted.
        """
        for hand in self.hands:
            if hand.get_value() >= 21:
                hand.set_complete()
                return 'stand'
            if not hand.is_complete():
                decision = strat(hand, count=True, running=self.count, true=self.get_true_count())
                hand.set_decision(decision)
                if decision == 'stand' or decision == 'surrender' or decision == 'double':
                    hand.set_complete()

    def new_shoe(self):
        self.count = 0
        self.num_cards_played = 0

    def update_count(self, card):
        """
        Update the count based on the value of the card.
        This method needs to be implemented based on the counting system being used.
        """

        self.num_cards_played += 1

        if card in self.inc_count:
            self.count+=1
        elif card in self.dec_count:
            self.count-=1
        else:
            assert card in self.no_count_change

    def get_true_count(self):
        assert self.num_cards_played > 0
        num_cards_left = NUM_CARDS_IN_DECK * self.num_decks - self.num_cards_played
        assert num_cards_left > 0
        return (self.count * num_cards_left) // NUM_CARDS_IN_DECK
    
class StrategicCounter(BasicCounter):
    """
    Represents a player using a strategic card counting system in addition to basic strategy in a game of Blackjack.
    """

    def __init__(self, gamestate):
        super().__init__(gamestate)
        self.base_bet = 1  # The base bet amount
        self.max_bet = 10  # The maximum bet amount

    def get_bet(self):
        """
        Determines the bet amount based on the true count.
        The betting strategy is to bet more when the count is favorable.
        """
        true_count = self.get_true_count()
        if true_count <= 1:
            return self.base_bet  # Minimum bet for unfavorable or neutral counts
        else:
            bet_amount = self.base_bet * (true_count - 1)  # Increase bet based on the true count
            return min(bet_amount, self.max_bet)  # Ensure the bet does not exceed the maximum
