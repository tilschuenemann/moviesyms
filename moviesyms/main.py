import pandas as pd
from pathlib import Path


def main(metadata_dir: Path, output_dir: Path):
    mapping = pd.read_csv(metadata_dir / "mapping.csv")
    mapping = mapping[["tmdb_id_auto", "disk_path"]].drop_duplicates()

    configuration = pd.DataFrame(
        {
            "metadata_file": ["production_countries.csv", "genres.csv", "crew.csv"],
            "subfolders_col": [
                "production_countries.name",
                "genres.name",
                "crew.name",
            ],
            "category": ["countries", "genres", "directors"],
        }
    )

    for index, row in configuration.iterrows():
        metadata_file = row["metadata_file"]
        subfolders_col = row["subfolders_col"]
        category = row["category"]

        metadata = pd.read_csv(metadata_dir / metadata_file)
        if category == "directors":
            metadata = metadata[metadata["crew.job"] == "Director"]

        subfolders = metadata[subfolders_col].unique().tolist()
        targets = metadata.merge(mapping, left_on="tmdb_id", right_on="tmdb_id_auto", how="left")

        for subfolder in subfolders:
            tmp_dir = output_dir / category / subfolder
            tmp_dir.mkdir(exist_ok=True, parents=True)

            tmp_linktab = targets[targets[subfolders_col] == subfolder]
            for index, row in tmp_linktab.iterrows():
                target = Path(row["disk_path"])
                link = tmp_dir / target.name
                link.symlink_to(target)
