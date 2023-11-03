class Dealer:
    """
    Represents the dealer in a game of Blackjack.
    """
    def __init__(self, card_one, card_two):
        self.cards = [card_one, card_two]  # The dealer's hand is represented as a list of cards.
        self.hand_value = self.calculate_hand_value()

    def get_upcard(self):
        """
        Returns the dealer's face-up card.
        """
        return self.cards[0]  # Assuming the first card is the face-up card.

    def calculate_hand_value(self):
        """
        Calculates the total value of the dealer's hand.
        """
        value = 0
        ace_count = 0

        for card in self.cards:
            if card in ['J', 'Q', 'K']:
                value += 10
            elif card == 'A':
                ace_count += 1
                value += 11  # Initially count aces as 11
            else:
                value += int(card)  # Assuming card is a string number

        # Adjust for aces if value is over 21
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1

        return value

    def is_blackjack(self):
        """
        Checks if the dealer has blackjack.
        """
        return self.hand_value == 21 and len(self.cards) == 2

    def hit(self, shoe):
        """
        Dealer takes a card from the shoe.
        """
        self.cards.append(shoe.deal())
        self.hand_value = self.calculate_hand_value()

    def play_hand(self, shoe):
        """
        Dealer plays their hand according to the casino rules, typically standing on 17 and above.
        """
        while self.hand_value < 17:
            self.hit(shoe)

    def get_value(self):
        """
        Returns the value of the dealer's hand.
        """
        return self.hand_value
