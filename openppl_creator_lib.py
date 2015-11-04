import os
import logging
import re
import sys

def get_oppl_files(path):
    oppl_files = {}

    logging.info("Reading source files...")
    logging.debug("Source path: %s", path)

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        if not os.path.isfile(file_path): 
            continue

        filename_without_extension, file_extension = os.path.splitext(file_name)
        if  file_extension != '.oppl':
            logging.debug("File extension not match: %s", file_extension)
            continue

        if os.stat(file_path).st_size == 0:
            logging.debug("File is empty: %s", file_path)
            continue

        logging.debug("Openning file: %s", file_path)
        with open(file_path, 'r') as file_:
            oppl_files[filename_without_extension] = file_.read()

    logging.info("Source files procesed...")
    return oppl_files



cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


def get_index(input_card):
    for index, card in enumerate(cards):
        if card == input_card:
            return index

def expand_pairs(index):
    return ['{0}{1}'.format(cards[i], cards[i]) for i in range(index + 1)]

def expand_not_pairs(card_index, is_suited_symbol):
    return ['{0}{1}{2}'.format(cards[card_index[0] ], cards[i], is_suited_symbol)
                for i in range(card_index[0] + 1 , card_index[1] + 1)]


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


