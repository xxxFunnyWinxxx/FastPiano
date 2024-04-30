import argparse
import pathlib
import json
import logging

from argparse import RawTextHelpFormatter

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)

SOURCE_FILE = pathlib.Path("data/music.json")


def append_data(source: pathlib.Path, dict_to_append: dict):
    if source.exists():
        with open(source, 'r') as f:
            data = json.load(f)
    else:
        logger.warning(f"{SOURCE_FILE} was not found. Initializing a new one.")
        data = []

    data.append(dict_to_append)

    with open(SOURCE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def remove_entries(source: pathlib.Path, file_name: str):
    if not SOURCE_FILE.exists():
        logger.error(f"File {SOURCE_FILE} does not exist.")
        return

    with open(SOURCE_FILE, 'r') as f:
        data = json.load(f)

    updated_data = [entry for entry in data if file_name not in entry]

    # Write the updated data back to the file
    with open(SOURCE_FILE, 'w') as f:
        json.dump(updated_data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(prog="MusicDataAppender", description="Append music collection", formatter_class=RawTextHelpFormatter)

    parser.add_argument("-f", "--file", help=f"name of file in corpus (default: None)", type=str, default=None)
    parser.add_argument("-a", "--author", help=f"author of music (default: None)", type=str, default=None)
    parser.add_argument("-n", "--name", help=f"name of music (default: None)", type=str, default=None)
    parser.add_argument("-p", "--purpose", help=f"purpose of learning (default: None)", type=str, default=None)
    parser.add_argument("-l", "--level", help=f"level of complexity (default: None)", type=str, default=None)
    parser.add_argument("--delete", help="delete all elements with the specified file name", type=str, default=None)

    args = parser.parse_args()

    dict_to_append = {args.file: {"file": args.file,
                                  "author": args.author,
                                  "name": args.name,
                                  "purpose": args.purpose,
                                  "level": args.level}}

    if args.delete:
        remove_entries(SOURCE_FILE, args.delete)
        logger.info(f"All entries with file name '{args.delete}' deleted from {SOURCE_FILE}.")
    else:
        append_data(SOURCE_FILE, dict_to_append)
        logger.info(f"Data {dict_to_append} appended to {SOURCE_FILE}.")


if __name__ == "__main__":
    main()
