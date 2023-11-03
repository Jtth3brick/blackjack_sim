import pandas as pd
from hand import Hand

basic_strat_df = pd.read_csv('basic_strat.csv')

NAME_MAP = {'P': 'pass',
            'S': 'stand',
            'H' : 'hit',
            'D' : 'double',
            'Sr' : 'surrender',
            }

def get_value(dataframe, row_label, column_label):
    return dataframe.loc[row_label, column_label]

def get_basic_strat(hand):
    cards = hand.get_cards()
    upcard = hand.get_upcard()

    if len(cards) == 2 and cards[0] == cards[1]:
        key = f"{cards[0]}s"
        if get_value(basic_strat_df, key, upcard) == 'Y':
            return 'split'
    
    if hand.get_num_soft_aces() >= 1:
        key = f"A{hand.get_value() - 1}"
        return NAME_MAP[get_value(basic_strat_df, key, upcard)]
    
    key = f"{hand.get_value()}"
    return NAME_MAP[get_value(basic_strat_df, key, upcard)]