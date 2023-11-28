from hand import Hand

class Game:
    """
    A sequence of Blackjack Rounds that keeps track of total money won or lost
    """
    def __init__(self, dealer_class, player_class, shoe, player_start_balance = 1e4, blackjack_payout=1.5):
        self.shoe = shoe
        self.player_balance = player_start_balance
        self.player_class = player_class
        self.dealer_class = dealer_class
        self.blackjack_payout = blackjack_payout

    def play_round(self):
        """
        Plays a round of Blackjack.
        """

        # initialize new dealer
        upcard = self.shoe.deal()
        dealer_downcard = self.shoe.deal(visible=False)
        dealer = self.dealer_class(upcard, dealer_downcard)
        dealer_upcard = dealer.get_upcard()
        assert dealer_upcard == upcard

        # start player new round and give hand + dealer upcard
        original_bet = self.player.new_round()
        assert original_bet > 0
        self.update_money(-original_bet)
        player_hands = [Hand(dealer_upcard, original_bet, self.shoe.deal(), self.shoe.deal())]
        self.player.set_hands(player_hands)
        self.player.play()

        # check for auto payout
        if player_hands[0].is_blackjack() and not (dealer_upcard in ['10', 'J', 'Q', 'K', 'A']):
            self.update_money(original_bet*(1 + self.blackjack_payout))
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
                        self.update_money(-1 * hand_bet)
                        if dealer.is_blackjack():
                            self.update_money(2 * hand_bet)
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
                        new_player_hand = Hand(player_hand.get_upcard(), original_bet, card1, self.shoe.deal())
                        player_hands.append(new_player_hand)
                    elif decision == 'surrender':
                        self.update_money(original_bet / 2)
                        player_hand.set_complete(force_loss=True)
            self.player.play()
        
        dealer.update_self(self.shoe)
        dealer_value = dealer.get_value()
        for player_hand in player_hands:
            hand_value = player_hand.get_value()
            if not player_hand.is_bust() and hand_value > dealer_value:
                self.update_money(2 * player_hand.get_bet_amount()) # player wins and gets double their bet
            elif not player_hand.is_bust() and hand_value == dealer_value:
                self.update_money(player_hand.get_bet_amount()) # player breaks even
        
        # finally notify player what downcard was
        self.player.update_count(dealer_downcard)

        return
    
    def play_game(self, num_games=1e4):
        """
        Plays a sequence of Blackjack rounds until the game count reaches GAMES.
        """
        self.player = self.player_class(self)
        self.shoe.assign_player(self.player)
        self.shoe.shuffle_shoe()
        for _ in range(num_games):
            if self.player.play_more():
                self.shoe.shuffle_if_cut()
                self.play_round()
            else:
                return self.player_balance()

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
