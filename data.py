import argparse
import logging

from argparse import RawTextHelpFormatter

from fastpiano.const import SOURCE_FILE
from fastpiano.data_parser import append_data, remove_entries

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(prog="MusicDataAppender", description="Append music collection", formatter_class=RawTextHelpFormatter)

    parser.add_argument("-f", "--file", help=f"name of file in corpus (default: None)", type=str, default=None)
    parser.add_argument("-a", "--author", help=f"author of music (default: None)", type=str, default=None)
    parser.add_argument("-n", "--name", help=f"name of music (default: None)", type=str, default=None)
    parser.add_argument("-p", "--purpose", help=f"purpose of learning (default: None)", type=str, default=None)
    parser.add_argument("-l", "--level", help=f"level of complexity (default: None)", type=str, default=None)
    parser.add_argument("--delete", help="delete all elements with the specified file name", type=str, default=None)

    args = parser.parse_args()

    if args.delete:
        remove_entries(SOURCE_FILE, args.delete)
        logger.info(f"All entries with file name '{args.delete}' deleted from {SOURCE_FILE}.")
    else:
        append_data(SOURCE_FILE, args.file, args.author, args.name, args.purpose, args.level)
        logger.info(f"Data {args.file} {args.author} {args.name} {args.purpose}{ args.level} appended to {SOURCE_FILE}.")


if __name__ == "__main__":
    main()
