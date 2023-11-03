class Hand:
    def __init__(self, dealer_upcard, bet, *cards):
        self.dealer_upcard = dealer_upcard
        self.bet = bet
        self.cards = list(cards)
        self.complete = False
        self.decision = None

    def add_card(self, card):
        self.cards.append(card)
        self.check_bust()

    def get_bet_amount(self):
        return self.bet

    def update_bet(self, new_bet):
        self.bet = new_bet

    def get_value(self):
        value, aces = 0, 0
        for card in self.cards:
            if card in 'JQK':
                value += 10
            elif card == 'A':
                aces += 1
            else:
                value += int(card)
        value += aces  # Add one for each ace.
        for _ in range(aces):
            # Upgrade an ace to 11 if possible.
            if value + 10 <= 21:
                value += 10
        return value
    
    def get_num_soft_aces(self):
        value, soft_aces = 0, 0
        for card in self.cards:
            if card in 'JQK':
                value += 10
            elif card != 'A':
                value += int(card)
        
        aces = self.cards.count('A')
        for _ in range(aces):
            # If adding 11 keeps us at or under 21, it's a soft Ace
            if value + 11 <= 21:
                value += 11
                soft_aces += 1
            else:
                # Otherwise, we have to add the Ace as 1
                value += 1
        
        return soft_aces

    def is_blackjack(self):
        return sorted([c if c != 'A' else '1' for c in self.cards]) == ['1', '10']

    def set_complete(self):
        self.complete = True

    def is_complete(self):
        return self.complete

    def check_bust(self):
        if self.get_value() > 21:
            self.set_complete()

    def set_decision(self, decision):
        # You would add the logic to check the decision here, possibly throwing an error if it's invalid
        self.decision = decision
        if decision not in ('hit', 'stand', 'double', 'split', 'surrender'):
            raise ValueError(f"Invalid decision: {decision}")

        # After a decision that finalizes the hand, set it as complete
        if decision in ('stand', 'double', 'surrender'):
            self.set_complete()

    def get_decision(self):
        return self.decision

    def end_hand(self):
        self.set_complete()

    def get_card(self, index):
        return self.cards[index]
    
    def get_upcard(self):
        return self.dealer_upcard

    def set_card(self, index, card):
        self.cards[index] = card

    def can_split(self):
        # Assuming that we can split the hand if the first two cards have the same value
        return len(self.cards) == 2 and self.cards[0] == self.cards[1]

    def can_double(self):
        # Typically doubling is only allowed on the first move, or on the first move after a split.
        return len(self.cards) == 2
    
    def get_cards(self):
        return self.cards

    def __repr__(self):
        return f"Hand({self.cards}, Bet: {self.bet}, Complete: {self.complete})"
