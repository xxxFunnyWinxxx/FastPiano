from music21 import corpus, environment
import json
from pathlib import Path
import logging

from fastpiano.const import COMPILER_FILE

environment.set('musescoreDirectPNGPath', COMPILER_FILE)

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def append_data(source: Path, file: str, author: str, name: str, purpose:str, level:str):
    dict_to_append = {"file": file,
                    "author": author,
                    "name": name,
                    "purpose": purpose,
                    "level": level}

    if source.exists():
        with open(source, 'r') as f:
            data = json.load(f)
    else:
        logger.warning(f"{source} was not found. Initializing a new one.")
        data = {}

    data[file] = dict_to_append

    with open(source, 'w') as f:
        json.dump(data, f, indent=2)


def remove_entries(source: Path, file_name: str):
    if not source.exists():
        logger.error(f"File {source} does not exist.")
        return

    with open(source, 'r') as f:
        data = json.load(f)

    updated_data = [entry for entry in data if file_name not in entry]

    with open(source, 'w') as f:
        json.dump(updated_data, f, indent=2)


def get_music_list(source: Path):
    if not source.exists():
        logger.error(f"File {source} does not exist.")
        return
    
    with open(source, 'r') as f:
        data = json.load(f)

    data_list = [tuple(row.values()) for row in data.values()]

    return data_list

def get_lines_from_file(images_dir: Path, file_name: str):
    if file_name.exists() and file_name.is_dir():
        files = [file for file in file_name.iterdir() if file.is_file()]
        return files
    else :
        corpus.parse(file_name)
        
