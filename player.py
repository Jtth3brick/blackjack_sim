from basic_strat import get_basic_strat
from hand import Hand

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
            if not hand.is_complete():
                decision = get_basic_strat(hand)
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

    def new_shoe():
        # Notifies player that a the shoe has been shuffled
        pass
