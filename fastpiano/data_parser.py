import json
import random
from pathlib import Path
import logging
import subprocess

from fastpiano.const import DATABASE_FILE, DATA_DIR, PDF_DIR, COMPILER_FILE


logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def append_data(
    file: str,
    author: str,
    name: str,
    purpose: str,
    level: str,
    source: str,
    database: Path = DATABASE_FILE,
):
    """
    Append data base with given score

    Parameters:
        - file (str): name of file
        - author (str): author of music
        - name (str): name of music
        - purpose (str): purpose of learning
        - level (str): level of complexity
        - source (str): where to find file (avaliable: corpus, data)
        - database (pathlib.Path) = DATABASE_FILE: .json data base file
    """
    dict_to_append = {
        "author": author,
        "name": name,
        "purpose": purpose,
        "level": level,
        "source": source,
    }

    if database.exists():
        with open(database, mode="r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        logger.warning(f"{database} was not found. Initializing a new one.")
        database.touch()
        data = {}

    data[file] = dict_to_append

    with open(database, mode="r", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def remove_entries(file: str, database: Path = DATABASE_FILE):
    """
    Remove data from data base by file name

    Parameters:
        - file (str): name of file
        - database (pathlib.Path) = DATABASE_FILE: .json data base file
    """
    if not database.exists():
        logger.error(f"File {database} does not exist.")
        return

    with open(database, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    updated_data = [entry for entry in data if file not in entry]

    with open(database, mode="r", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2)


def get_music_list(database: Path = DATABASE_FILE):
    """
    Returns list of avaliable music in data base

    Parameters:
        - database (pathlib.Path) = DATABASE_FILE: .json data base file

    Return:
        list[tuple]: avaliable music in format [(file, author, name, purpose, level, source)]

    Warning:
        Retun None, if source wasn't found
    """
    if not database.exists():
        logger.error(f"File {database} does not exist.")
        return

    with open(database, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    data_list = [(key, *row.values()) for key, row in data.items()]

    return data_list


def get_pdf_from_file(
    file: str, pdf_dir: Path = PDF_DIR, data_dir: Path = DATA_DIR, database: Path = DATABASE_FILE
):
    """
    Returns pdf file location

    Parameters:
        - file (str): pdf file name
        - pdf_dir (pathlib.Path) = PDF_DIR: pdf files directory
        - data_dir (pathlib.Path) = DATA_DIR: data files directory
        - database (pathlib.Path) = DATABASE_FILE: .json data base file

    Return:
        str: pdf file location
    """
    if database.exists():
        with open(database, mode="r", encoding="utf-8") as f:
            music = json.load(f)
    else:
        logger.warning(f"{database} was not found.")
        return None

    if file in music:
        source = music[file]["source"]
    else:
        logger.warning(f"No file {file} in {database}.")
        return None

    pdf_file = pdf_dir / f"{Path(file).stem}.pdf"
    data_file = data_dir / file
    if source == "pdf":
        if pdf_file.exists() and pdf_file.is_file():
            return pdf_file
        else:
            logger.warning(
                f"No pdf file {pdf_file}. exist {data_file.exists()}, is_file {data_file.is_file()}"
            )
            return None
    elif source == "data":
        if pdf_file.exists() and pdf_file.is_file():
            return pdf_file
        proc = subprocess.Popen(
            [COMPILER_FILE, "-o", pdf_file, data_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        logger.debug(f"MuseScore output: {out}, error {err}")
        return pdf_file
    else:
        logger.warning(f"Unknown source of data {source}")
        return None


def get_random_file(purpose: str, level: str, database: Path = DATABASE_FILE):
    """
    Returns random file from database with appropriate purpose and level

    Parameters:
        - purpose (str): purpose parameter
        - level (str): level parameter
        - database (pathlib.Path) = DATABASE_FILE: .json data base file

    Return:
        str: pdf file location
    """
    if database.exists():
        with open(database, mode="r", encoding="utf-8") as f:
            music = json.load(f)
    else:
        logger.warning(f"{database} was not found.")
        return None

    filtered_files = [
        key
        for key, value in music.items()
        if value["purpose"] == purpose and value["level"] == level
    ]

    if not filtered_files:
        logger.warning(f"No appropriate file for purpose: {purpose}, level: {level}.")
        return None

    random_file = random.choice(filtered_files)

    return random_file
