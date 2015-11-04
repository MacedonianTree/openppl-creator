import os
import logging

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
