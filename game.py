from hand import Hand
import logging

# Custom filter to ignore messages from a specific library
class FilterOutMatplotlib(logging.Filter):
    def filter(self, record):
        return ('matplotlib' not in record.name)
# Configure logging
logging.basicConfig(filename='blackjack.log', level=logging.DEBUG,
                    format='%(levelname)s: %(message)s')

# Get the root logger
logger = logging.getLogger()

# Apply the filter to the root logger
logger.addFilter(FilterOutMatplotlib())

class Game:
    """
    A sequence of Blackjack Rounds that keeps track of total money won or lost
    """
    def __init__(self, dealer_class, player_class, shoe_class, player_start_balance = 1e4, blackjack_payout=1.5, num_decks=6):
        self.shoe_class = shoe_class
        self.player_balance = player_start_balance
        self.player_class = player_class
        self.dealer_class = dealer_class
        self.blackjack_payout = blackjack_payout
        self.num_decks = num_decks

    def play_round(self):
        """
        Plays a round of Blackjack.
        """

        initial_balance = self.player_balance
        original_bet = self.player.new_round()
        assert original_bet > 0
        self.update_money(-original_bet, "Initial bet")

        # initialize new dealer
        upcard = self.shoe.deal()
        dealer_downcard = self.shoe.deal(visible=False)
        dealer = self.dealer_class(upcard, dealer_downcard)

        player_hands = [Hand(upcard, original_bet, self.shoe.deal(), self.shoe.deal())]
        self.player.set_hands(player_hands)
        self.player.play()

        is_blackjack = False
        if player_hands[0].is_blackjack() and not dealer.is_blackjack():
            self.update_money(original_bet * (1 + self.blackjack_payout), "Blackjack payout")
            is_blackjack = True

        def update_log():
            running_count = None
            true_count = None
            if hasattr(self.player, 'count'):
                running_count = self.player.count
                true_count = self.player.get_true_count()
                
            logger.info(f"Player hands: {player_hands}, Running count: {running_count}, True Count: {true_count}")
            return running_count, true_count

        while not self.round_over(player_hands, is_blackjack):
            update_log()
            for i, player_hand in enumerate(player_hands):
                if not player_hand.is_complete():
                    hand_bet = player_hand.get_bet_amount()
                    decision = player_hand.get_decision()
                    if decision == 'hit':
                        player_hand.add_card(self.shoe.deal())
                    elif decision == 'insure':
                        self.update_money(-hand_bet, "Insurance bet")
                        if dealer.is_blackjack():
                            self.update_money(2 * hand_bet, "Insurance payout")
                            [player_hand.end_hand() for player_hand in player_hands]
                    elif decision == 'double':
                        self.update_money(-hand_bet, "Double down bet")
                        player_hand.update_bet(hand_bet * 2)
                        player_hand.add_card(self.shoe.deal())
                        player_hand.set_complete()
                    elif decision == 'split':
                        card0 = player_hand.get_card(0)
                        card1 = player_hand.get_card(1)
                        player_hand.set_card(1, self.shoe.deal())
                        self.update_money(-original_bet, "Splitting bet")
                        new_player_hand = Hand(player_hand.get_upcard(), original_bet, card1, self.shoe.deal())
                        player_hands.append(new_player_hand)
                    elif decision == 'surrender':
                        self.update_money(original_bet / 2, "Surrender")
                        player_hand.set_complete(force_loss=True)
            self.player.play()
        
        dealer.update_self(self.shoe)
        dealer_value = dealer.get_value()
        for player_hand in player_hands:
            hand_value = player_hand.get_value()
            if not player_hand.is_bust() and self.is_bust(dealer_value) and not is_blackjack:
                self.update_money(2 * player_hand.get_bet_amount(), "Dealer busts, player wins")
            elif not player_hand.is_bust() and hand_value > dealer_value and not is_blackjack:
                self.update_money(2 * player_hand.get_bet_amount(), "Player wins")
            elif not player_hand.is_bust() and hand_value == dealer_value and not is_blackjack:
                self.update_money(player_hand.get_bet_amount(), "Push - player breaks even")

        self.player.update_count(dealer_downcard)
        running_count, true_count = update_log()
        logger.info(f"Player notified of round's downcard: {dealer_downcard}\n\t- Final dealer state: {dealer}\n\t- Final running count: {running_count}\n\t- Final true count: {true_count}\n\t- Num cards: {len(self.shoe.cards)}")
        logger.info("End of round: Initial balance: %s, Ending balance: %s, Hands: %s",
                    initial_balance, self.player_balance, player_hands)
        
        

    
    def play_game(self, num_games=1e4):
        """
        Plays a sequence of Blackjack rounds until the game count reaches GAMES.
        """
        logger.info("---------------------------------------------------------- NEW DAY ----------------------------------------------------------")
        self.player = self.player_class(self)
        self.shoe = self.shoe_class(self.num_decks)
        self.shoe.assign_player(self.player)
        self.shoe.shuffle_shoe()
        for _ in range(num_games):
            if self.player.play_more():
                logger.info("---------------------------------------------------------- NEW HAND ----------------------------------------------------------")
                self.shoe.shuffle_if_cut()
                self.play_round()
            else:
                return self.player_balance
        return self.player_balance

    def update_money(self, amount, reason=""):
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a numerical value")
        new_balance = self.player_balance + amount
        if new_balance <= 0:
            raise ValueError("player can't bet this amount")
        self.player_balance = new_balance
        logger.info("Balance change: %s, New balance: %s, Reason: %s", amount, new_balance, reason)

    def round_over(self, player_hands, is_blackjack):
        if is_blackjack:
            return True
        for player_hand in player_hands:
            if not player_hand.is_complete():
                return False
        return True
    
    def get_player_balance(self):
        return self.player_balance
    
    @staticmethod
    def is_bust(value):
        return value > 21
