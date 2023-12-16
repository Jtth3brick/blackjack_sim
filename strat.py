import pandas as pd

NAME_MAP = {
    'P': 'pass',
    'S': 'stand',
    'H': 'hit',
    'D': 'double',
    'Sr': 'surrender',
    # 'Sr': 'stand',
}

DEVIATIONS = {
    ('17', '8'): {'condition': lambda t, r: r >= 4, 'action': 'Sr'},
    ('17', '9'): {'condition': lambda t, r: t <= -1, 'action': 'S'},
    ('15', '9'): {'condition': lambda t, r: r >= 2, 'action': 'Sr'},
    ('15', '10'): {'condition': lambda t, r: r <= 0, 'action': 'S'},
    ('15', 'A'): {'condition': lambda t, r: r >= 2, 'action': 'Sr'},
    ('A8', '4'): {'condition': lambda t, r: t >= 3, 'action': 'D'},
    ('A8', '5'): {'condition': lambda t, r: t >= 1, 'action': 'D'},
    ('A6', '2'): {'condition': lambda t, r: t >= 1, 'action': 'D'},
    ('16', '9'): {'condition': lambda t, r: r >= 4, 'action': 'S'},
    ('13', '2'): {'condition': lambda t, r: r <= -1, 'action': 'H'},
    ('12', '2'): {'condition': lambda t, r: r >= 3, 'action': 'S'},
    ('12', '3'): {'condition': lambda t, r: r >= 2, 'action': 'S'},
    ('12', '4'): {'condition': lambda t, r: r <= 0, 'action': 'H'},
    ('10', '10'): {'condition': lambda t, r: r >= 4, 'action': 'D'},
    ('10', 'A'): {'condition': lambda t, r: r >= 4, 'action': 'D'},
    ('9', '2'): {'condition': lambda t, r: t >= 1, 'action': 'D'},
    ('9', '7'): {'condition': lambda t, r: t >= 3, 'action': 'D'},
    ('8', '6'): {'condition': lambda t, r: t >= 2, 'action': 'D'}
}

def get_value(dataframe, row_label, column_label):
    return dataframe.loc[row_label, column_label]

def check_deviation(key, upcard, running_count, true_count):
    if (key, upcard) in DEVIATIONS:
        deviation = DEVIATIONS[(key, upcard)]
        condition_func = deviation['condition']
        action = deviation['action']

        # Evaluate the condition using the lambda function
        if condition_func(true_count, running_count):
            return action

    return None
    

def strat(hand, count=False, running=0, true=0):
    csv_path = 'basic_strat.csv'
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

    # Check for deviations before defaulting to basic strategy
    deviation_action = check_deviation(key, upcard, running, true)
    if deviation_action:
        return NAME_MAP[deviation_action]

    return NAME_MAP[get_value(dataframe, key, upcard)]
