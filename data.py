import argparse
import logging

from argparse import RawTextHelpFormatter

from fastpiano.data_parser import append_data, remove_entries

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(prog="MusicDataAppender", description="Append music collection", formatter_class=RawTextHelpFormatter)

    parser.add_argument("-f", "--file", help=f"name of file (default: None)", type=str, default=None)
    parser.add_argument("-a", "--author", help=f"author of music (default: None)", type=str, default=None)
    parser.add_argument("-n", "--name", help=f"name of music (default: None)", type=str, default=None)
    parser.add_argument("-p", "--purpose", help=f"purpose of learning (default: None)", type=str, default=None)
    parser.add_argument("-l", "--level", help=f"level of complexity (default: None)", type=str, default=None)
    parser.add_argument("-s", "--source", help=f"where to find file (avaliable: data, pdf) (default: pdf)", type=str, default='pdf')
    parser.add_argument("--delete", help="delete all elements with the specified file name", type=str, default=None)

    args = parser.parse_args()

    if args.delete:
        remove_entries(args.delete)
        logger.info(f"All entries with file name '{args.delete}' deleted from data base.")
    else:
        append_data(args.file, args.author, args.name, args.purpose, args.level, args.source)
        logger.info(f"Data {args.file} {args.author} {args.name} {args.purpose} {args.level} {args.source} appended to data base.")


if __name__ == "__main__":
    main()
