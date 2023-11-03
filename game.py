from hand import Hand

class Game:
    """
    A sequence of Blackjack Rounds that keeps track of total money won or lost
    """
    def __init__(self, dealer_class, player_class, shoe, player_start_balance = 1e4):
        self.shoe = shoe
        self.player_balance = player_start_balance
        self.player_class = player_class
        self.dealer_class = dealer_class

    def play_round(self):
        """
        Plays a round of Blackjack.
        """

        # initialize new dealer
        dealer = self.dealer_class(self.shoe.deal(), self.shoe.deal())
        dealer_upcard = dealer.get_upcard()

        # start player new round and give hand + dealer upcard
        original_bet = self.player.new_round()
        assert original_bet > 0
        self.update_money(-original_bet)
        player_hands = [Hand(dealer_upcard, original_bet, self.shoe.deal(), self.shoe.deal())]
        self.player.set_hands(player_hands)
        self.player.play()

        # check for auto payout
        if player_hands[0].is_blackjack() and not (dealer_upcard in ['10', 'J', 'Q', 'K', 'A']):
            self.update_money(original_bet)
            return
        
        # loop until all player hands are in end case
        while not self.round_over(player_hands):
            for player_hand in player_hands:
                if player_hand.is_complete():
                    pass
                else:
                    hand_bet = player_hand.get_bet_amount()
                    decision = player_hand.get_decision()
                    if decision == 'hit':
                        player_hand.add_card(self.shoe.deal())
                    elif decision == 'insure':
                        self.update_money(hand_bet)
                        if dealer.is_blackjack():
                            self.update_money(hand_bet)
                            [player_hand.end_hand() for player_hand in player_hands]
                    elif decision == 'double':
                        self.update_money(-hand_bet)
                        player_hand.update_bet(hand_bet * 2)
                        player_hand.add_card(self.shoe.deal())
                        player_hand.set_complete()
                    elif decision == 'split':
                        card0 = player_hand.get_card(0)
                        card1 = player_hand.get_card(1)
                        player_hand.set_card(1, self.shoe.deal())
                        self.update_money(-original_bet)
                        new_player_hand = Hand(original_bet, card1, self.shoe.deal())
                        player_hands.append(new_player_hand)
                    elif decision == 'surrender':
                        self.update_money(original_bet / 2)
            self.player.play()
        
        dealer.update_self(self.shoe)
        dealer_value = dealer.get_value()
        for player_hand in player_hands:
            hand_value = player_hand.get_value()
            if not self.is_bust(hand_value) and hand_value > dealer_value:
                self.update_money(player_hand.get_bet_amount())

        return
    
    def play_game(self, num_games=1e4):
        """
        Plays a sequence of Blackjack rounds until the game count reaches GAMES.
        """
        self.player = self.player_class(self)
        for _ in range(num_games):
            shuffled = self.shoe.shuffle_if_cut()
            if shuffled:
                self.player.new_shoe()
            self.play_round()

        return self.player_balance

    def update_money(self, amount):
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a numerical value")
        new_balance = self.player_balance + amount
        if new_balance <= 0:
            raise ValueError("player can't bet this amount")
        self.player_balance = new_balance

    def round_over(self, player_hands):
        for player_hand in player_hands:
            if not player_hand.is_complete():
                return False
        return True
    
    def get_player_balance(self):
        return self.player_balance
    
    @staticmethod
    def is_bust(value):
        return value > 21
