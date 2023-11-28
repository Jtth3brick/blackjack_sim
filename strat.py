import pandas as pd

NAME_MAP = {
    'P': 'pass',
    'S': 'stand',
    'H': 'hit',
    'D': 'double',
    'Sr': 'surrender',
}

def get_value(dataframe, row_label, column_label):
    return dataframe.loc[row_label, column_label]
    

def get_csv_path(count, running, true):

    assert int(true) == true
    assert int(running) == running

    if running == 0 or not count:
        assert true == 0

        return 'strat_csvs/basic_strat.csv'
    elif true == 0 and running > 0:
        return 'strat_csvs/basic_strat_running_positive.csv'
    elif true == 0 and running < 0:
        return 'strat_csvs/basic_strat_running_negative.csv'
    elif true > 0 and true <= 6
        return f"strat_csvs/basic_strat_true_{true}.csv"
    elif true == -1 or true < 0
        return f"strat_csvs/basic_strat_true_negative_1.csv"
    elif true > 6:
        return 'strat_csvs/basic_strat_true_6.csv'
    
    raise ValueError(f"can't find csv path for\n\tcount={count}\n\trunning={running}\n\ttrue={true}")

def strat(hand, count=False, running=0, true=0):
    csv_path = get_csv_path(count, running, true)
    dataframe = pd.read_csv(csv_path, index_col=0)

    cards = hand.get_cards()
    upcard = str(hand.get_upcard_val())  # Ensure upcard is a string

    if hand.can_split():
        if cards[0] in 'JQK':
            key = '10s'
        else:
            key = f"{cards[0]}s"  # Assuming cards is a list of strings
        if get_value(dataframe, key, upcard) == 'Y':
            return 'split'
    
    if hand.get_num_soft_aces() >= 1:
        # This assumes that `hand.get_value() - 10` is the correct logic for your soft hand representation
        key = f"A{hand.get_value() - 10}"
        return NAME_MAP[get_value(dataframe, key, upcard)]
    
    # If none of the above, use the hand's total value as the key
    key = str(hand.get_value())  # Make sure this matches the DataFrame's index

    return NAME_MAP[get_value(dataframe, key, upcard)]
