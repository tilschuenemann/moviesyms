import argparse
import pathlib
from moviesyms.main import Moviesyms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata_dir", nargs=1, type=pathlib.Path, help="")
    parser.add_argument("output_dir", nargs=1, type=pathlib.Path, help="")
    parser.add_argument("--diary", nargs=1, type=pathlib.Path, help="")
    args = parser.parse_args()

    m = Moviesyms(args.metadata_dir[0], args.output_dir[0], args.diary[0])
    m.create_countries()
    m.create_decade()
    m.create_genres()
    m.create_runtime()
    m.create_spoken_languages()
    m.create_directors()

    m.create_last_seen_in()
    m.create_ratings()


if __name__ == "__main__":
    main()
