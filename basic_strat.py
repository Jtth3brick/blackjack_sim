import pandas as pd

basic_strat_df = pd.read_csv('strat_csvs/basic_strat_true_zero.csv', index_col=0)

NAME_MAP = {
    'P': 'pass',
    'S': 'stand',
    'H': 'hit',
    'D': 'double',
    'Sr': 'surrender',
}

def get_value(dataframe, row_label, column_label):
    return dataframe.loc[row_label, column_label]

def get_basic_strat(hand):
    cards = hand.get_cards()
    upcard = str(hand.get_upcard_val())  # Ensure upcard is a string

    if hand.can_split():
        if cards[0] in 'JQK':
            key = '10s'
        else:
            key = f"{cards[0]}s"  # Assuming cards is a list of strings
        if get_value(basic_strat_df, key, upcard) == 'Y':
            return 'split'
    
    if hand.get_num_soft_aces() >= 1:
        # This assumes that `hand.get_value() - 10` is the correct logic for your soft hand representation
        key = f"A{hand.get_value() - 10}"
        return NAME_MAP[get_value(basic_strat_df, key, upcard)]
    
    # If none of the above, use the hand's total value as the key
    key = str(hand.get_value())  # Make sure this matches the DataFrame's index

    return NAME_MAP[get_value(basic_strat_df, key, upcard)]
