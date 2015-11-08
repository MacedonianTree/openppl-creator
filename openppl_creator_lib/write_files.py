import logging


def hand_lists_percentages(hand_percentages, hands_file_path, original_script):

    new_lines = []
    list_index = 0

    logging.info('Overwriting hand lists file.')
    for line in original_script.split('\n'):
        new_lines.append(line)
        
        if line.startswith('##list'):
            new_lines.append('// {0:.2f} %'.format(hand_percentages[list_index]))
            list_index += 1
            continue

        if line.startswith('##'):
            logging.debug('Skiping  add percentage in line: %s', line)
            list_index += 1            
            continue

    script_with_percetanges = '\n'.join(new_lines)

    with open(hands_file_path, 'w') as hands_file: 
        hands_file.write(script_with_percetanges)

    logging.info('Done!')