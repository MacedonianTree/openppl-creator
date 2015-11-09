import os
import logging

def get_oppl_files(path):
    oppl_files = {}

    logging.info("Reading source files...")
    logging.debug("Source path: %s", path)

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        if not os.path.isfile(file_path):
            oppl_files.update(get_oppl_files(file_path))
            continue

        if os.stat(file_path).st_size == 0:
            logging.info("File is empty: %s", file_path)

        filename_without_extension, file_extension = os.path.splitext(file_name)
        if  not file_extension in ['.oppl', '.ohf']:
            logging.debug("File extension not match: %s", file_extension)
            continue

        logging.debug("Openning file: %s", file_path)
        with open(file_path, 'r') as file_:
            oppl_files[filename_without_extension] = file_.read()

    logging.info("Source files procesed...")
    return oppl_files