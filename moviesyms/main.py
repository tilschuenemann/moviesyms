import pandas as pd
import pathlib
import datetime
import math

from movieparse.main import movieparse
from moviesyms.LetterboxdDiary import LetterboxdDiary


class Moviesyms:
    def __init__(self, metadata_dir: pathlib.Path, output_dir: pathlib.Path, diary: pathlib.Path = None):
        if metadata_dir.is_dir() is False:
            exit("metadata should be a folder!")

        if output_dir.is_dir() is False:
            exit("output_dir should be a folder!")
        self.__output_dir = output_dir

        self.m = movieparse(metadata_dir, metadata_dir)
        self.mapping_diary = pd.DataFrame()

        self._init_mapping()
        self._init_diary(diary)

    def _init_mapping(self):
        self.mapping = self.m.cached_mapping[["disk_path", "tmdb_id"]].copy()
        self.mapping["disk_path"] = self.mapping["disk_path"].apply(lambda x: pathlib.Path(x))
        self.mapping["name"] = self.mapping["disk_path"].apply(lambda x: x.name)

    def _init_diary(self, diary_path: pathlib.Path):
        """Diary record need to be joined onto mapping.csv with a user naming convention.
        We emulate all conventions and then choose the one with most matches in mapping.csv.

        After merging all unecessary / duplicate columns are dropped and "watched" is determined (NaT!=NaT)."""
        if diary_path is None or diary_path.exists() is False:
            return

        diary = pd.read_csv(
            diary_path,
            parse_dates=["date", "watched_date"],
            header=0,
            names=[
                "date",
                "name",
                "year",
                "letterboxd_uri",
                "rating",
                "rewatch",
                "tags",
                "watched_date",
            ],
        ).to_dict()
        diary = pd.DataFrame(LetterboxdDiary(diary))

        diary["last_seen_in"] = diary["watched_date"].dt.year
        diary["style0"] = diary["year"].astype(str) + " " + diary["name"]
        diary["style1"] = diary["year"].astype(str) + " - " + diary["name"]
        diary["watched"] = diary["watched_date"] == diary["watched_date"]
        diary["rating"] = diary["rating"].apply(lambda x: f"{x:.1f}")
        diary["last_seen_in"] = diary["last_seen_in"].apply(lambda x: f"{x:.0f}")

        self.diary = diary

        user_conv = set(self.mapping["name"])
        s0 = user_conv - set(self.diary["style0"])
        s1 = user_conv - set(self.diary["style1"])

        if s0 == min(s0, s1):
            right_on = "style0"
            print(f"matched {(len(s0))} of {(len(user_conv))} using style0")
        elif s1 == min(s0, s1):
            right_on = "style1"
            print(f"matched {(len(s01))} of {(len(user_conv))} using style1")

        self.mapping_diary = self.mapping.merge(
            self.diary, how="left", left_on="name", right_on=right_on, suffixes=[None, "_y"]
        ).drop(columns=["style0", "style1", "name", "name_y", "year"], axis=0)

    def _check_mapping(self):
        if self.mapping.empty:
            exit("mapping in metadata_dir is empty!")

    def _check_diary(self):
        if self.mapping_diary.empty:
            exit("diary is empty!")
        elif sum(pd.notnull(self.mapping_diary["letterboxd_uri"])) == 0:
            exit("merging mapping and diary yields zero matches!")

    def create_countries(self):
        subfolders_col = "production_countries.name"
        df = self.m.prod_count[["tmdb_id", subfolders_col]].copy()

        df = df.merge(self.mapping[["disk_path", "tmdb_id"]], left_on="tmdb_id", right_on="tmdb_id", how="left")
        self._create_symlinks("countries", subfolders_col, df)

    def create_genres(self):
        subfolders_col = "genres.name"
        df = self.m.genres[["tmdb_id", subfolders_col]].copy()

        df = df.merge(self.mapping[["disk_path", "tmdb_id"]], left_on="tmdb_id", right_on="tmdb_id", how="left")
        self._create_symlinks("genres", subfolders_col, df)

    def create_directors(self):
        subfolders_col = "crew.name"
        df = self.m.crew[["tmdb_id", subfolders_col, "crew.job"]].copy()

        df = df[df["crew.job"] == "Director"]

        df = df.merge(self.mapping[["disk_path", "tmdb_id"]], left_on="tmdb_id", right_on="tmdb_id", how="left")
        self._create_symlinks("directors", subfolders_col, df)

    def create_spoken_languages(self):
        subfolders_col = "spoken_languages.english_name"
        df = self.m.spoken_langs[["tmdb_id", subfolders_col]].copy()
        df = df.merge(self.mapping[["disk_path", "tmdb_id"]], left_on="tmdb_id", right_on="tmdb_id", how="left")

        self._create_symlinks("spoken_languages", subfolders_col, df)

    def create_runtime(self):
        subfolders_col = "m.runtime"
        df = self.m.details[["tmdb_id", subfolders_col]].copy()

        df["m.runtime"] = df["m.runtime"].apply(lambda x: math.ceil(x / 30) * 30).astype(str)

        df = df.merge(self.mapping[["disk_path", "tmdb_id"]], left_on="tmdb_id", right_on="tmdb_id", how="left")
        self._create_symlinks("runtime", subfolders_col, df)

    def create_decade(self):
        subfolders_col = "m.release_date"
        df = self.m.details[["tmdb_id", subfolders_col]].copy()

        df["m.release_date"] = pd.to_datetime(df["m.release_date"])
        df["m.release_date"] = df["m.release_date"].dt.year.apply(lambda x: int(x / 10) * 10).astype(str)

        df = df.merge(self.mapping[["disk_path", "tmdb_id"]], left_on="tmdb_id", right_on="tmdb_id", how="left")
        self._create_symlinks("decade", subfolders_col, df)

    def create_last_seen_in(self):
        self._check_diary()
        subfolders_col = "last_seen_in"
        df = self.mapping_diary[["disk_path", subfolders_col]].copy()

        # drop unseen movies
        df = df[df["last_seen_in"] != "nan"]
        df = df.drop_duplicates(subset=["disk_path"], keep="last")

        self._create_symlinks("last_seen_in", subfolders_col, df)

    def create_ratings(self):
        self._check_diary()

        subfolders_col = "rating"
        df = self.mapping_diary[["disk_path", subfolders_col]].copy()

        # drop unseen movies
        df = df[df["rating"] != "nan"]
        df = df.drop_duplicates(subset=["disk_path"], keep="last")

        self._create_symlinks("rating", subfolders_col, df)

    def _create_symlinks(self, category: str, subfolders_col: str, targets: pd.DataFrame):
        for subfolder in set(targets[subfolders_col]):
            tmp_dir = self.__output_dir / category / subfolder
            tmp_dir.mkdir(exist_ok=True, parents=True)

            tmp_linktab = targets[targets[subfolders_col] == subfolder]
            for index, row in tmp_linktab.iterrows():
                target = row["disk_path"]
                link = tmp_dir / target.name
                link.symlink_to(target, target_is_directory=True)
