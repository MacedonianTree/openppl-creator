import re
import sys
import logging
import numpy


cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def expand_hands(script):
    while True:
        match = re.search(r'(?!^\/\/)[AKQJT2-9][AKQJT2-9][so]?\+', script)
        
        if not match:
            break
    
        hand_to_expand = match.group(0)
    
        card_index = [get_index(hand_to_expand[i]) for i in range(2)]
        
        if card_index[0] > card_index[1]:
            sys.exit("ERROR:Hand bad defined, firts card must be the big one: %s", hand_to_expand)

        if card_index[0] == card_index[1]:
            expanded_hand_list = expand_pairs(card_index[0])
        else:
            expanded_hand_list = expand_not_pairs(card_index, hand_to_expand[2])
    
        expanded_hand = ' '.join(expanded_hand_list)

        script = script.replace(hand_to_expand, expanded_hand)

    return script

def get_index(input_card):
    for index, card in enumerate(cards):
        if card == input_card:
            return index

def expand_pairs(index):
    return ['{0}{1}'.format(cards[i], cards[i]) for i in range(index + 1)]

def expand_not_pairs(card_index, is_suited_symbol):
    return ['{0}{1}{2}'.format(cards[card_index[0] ], cards[i], is_suited_symbol)
                for i in range(card_index[0] + 1 , card_index[1] + 1)]

def add_percentage_hands(script):
    logging.info('Adding percentage hands...')

    hands_range, combinations = get_hands_range_and_combinations()

    accumulate_combinations_array = numpy.add.accumulate(combinations)
    total_combinations = accumulate_combinations_array[-1]

    for percentage in range(0,101):
        hand_combinations = total_combinations * percentage /100
        hand_range_index = get_hand_range_index(hand_combinations, accumulate_combinations_array)
        hand_header = '\n\n##list{0}##\n'.format(percentage)
        hand_text = ' '.join(hands_range[:hand_range_index])
        script = script + hand_header + hand_text

    return script

def get_hands_percentage(expanded_hands):
    hands_pattern = re.compile('(?!^\/\/)[AKQJT2-9][AKQJT2-9][so]?')
    
    logging.info('Calculating hand lists percentages...')
    hand_list = []
    hands_percentages = []
    for line in expanded_hands.split('\n'):
        if line.startswith('##'):
            hands_percentages.append(calculate_hands_percentage(hand_list))
            hand_list = []
    
            if line.startswith('##list'):
                continue

            if line.startswith('##f$'):
                logging.error("Function find in hand list, please check it.")
                continue
        
            if line.startswith('##'):
                logging.error("Bad function declaration in hand lists.")
                continue
        
        if line.startswith('//'):
            continue
        
        hand_list.extend(hands_pattern.findall(line))

    hands_percentages.append(calculate_hands_percentage(hand_list))

    return hands_percentages[1:]

def get_hands_range_and_combinations():
    hands_range = ['AA', 'KK', 'QQ', 'AKs', 'JJ', 'AQs', 'KQs', 'AJs', 'KJs', 'TT', 'AKo', 'ATs', 'QJs', 'KTs', 'QTs', 'JTs', '99', 'AQo', 'A9s', 'KQo', '88', 'K9s', 'T9s', 'A8s', 'Q9s', 'J9s', 'AJo', 'A5s', '77', 'A7s', 'KJo', 'A4s', 'A3s', 'A6s', 'QJo', '66', 'K8s', 'T8s', 'A2s', '98s', 'J8s', 'ATo', 'Q8s', 'K7s', 'KTo', '55', 'JTo', '87s', 'QTo', '44', '33', '22', 'K6s', '97s', 'K5s', '76s', 'T7s', 'K4s', 'K3s', 'K2s', 'Q7s', '86s', '65s', 'J7s', '54s', 'Q6s', '75s', '96s', 'Q5s', '64s', 'Q4s', 'Q3s', 'T9o', 'T6s', 'Q2s', 'A9o', '53s', '85s', 'J6s', 'J9o', 'K9o', 'J5s', 'Q9o', '43s', '74s', 'J4s', 'J3s', '95s', 'J2s', '63s', 'A8o', '52s', 'T5s', '84s', 'T4s', 'T3s', '42s', 'T2s', '98o', 'T8o', 'A5o', 'A7o', '73s', 'A4o', '32s', '94s', '93s', 'J8o', 'A3o', '62s', '92s', 'K8o', 'A6o', '87o', 'Q8o', '83s', 'A2o', '82s', '97o', '72s', '76o', 'K7o', '65o', 'T7o', 'K6o', '86o', '54o', 'K5o', 'J7o', '75o', 'Q7o', 'K4o', 'K3o', '96o', 'K2o', '64o', 'Q6o', '53o', '85o', 'T6o', 'Q5o', '43o', 'Q4o', 'Q3o', '74o', 'Q2o', 'J6o', '63o', 'J5o', '95o', '52o', 'J4o', 'J3o', '42o', 'J2o', '84o', 'T5o', 'T4o', '32o', 'T3o', '73o', 'T2o', '62o', '94o', '93o', '92o', '83o', '82o', '72o']

    combinations = []
    for i in hands_range:
        if is_pair(i):
            combinations.append(6)
        elif is_suited(i):
            combinations.append(4)
        else:
            combinations.append(12)

    return hands_range, combinations

def is_pair(hand):
    return (hand[0] == hand[1])

def is_suited(hand):
    return (hand[2] == 's')
            
def get_hand_range_index(hand_combinations, accumulate_combinations_array):
    
    hand_range_index = 0
    for idx, accumulate_combinations in enumerate(accumulate_combinations_array):
        if hand_combinations < accumulate_combinations:
            break
        hand_range_index = idx

    return hand_range_index

def calculate_hands_percentage(hand_list):

    hands_range, combinations = get_hands_range_and_combinations()

    total_combinations = numpy.sum(combinations)

    hand_combinations = 0
    for hand in hand_list:
        for idx, hand_range in enumerate(hands_range):
            if hand == hand_range:
                hand_combinations += combinations[idx]
                break

    hands_percentage = (hand_combinations * 100)/ total_combinations

    return hands_percentage