import pytest
from moviesyms.main import Moviesyms
import pathlib


def check_for_correct_symlinks_in_subdir(subdir_path):
    symlink_list = []
    for x in subdir_path.iterdir():
        if x.is_symlink():
            symlink_list.append(x.name)

    assert set(symlink_list) == set(["1999 The Matrix"])
    assert len(symlink_list) == 1


@pytest.fixture
def tmp_output(tmp_path):
    tmp_dir = tmp_path / "output"
    tmp_dir.mkdir()
    return tmp_dir


@pytest.fixture
def setup_moviesyms(tmp_output):
    metadata_dir = pathlib.Path("tests/data")
    m = Moviesyms(metadata_dir, tmp_output)
    return m


@pytest.fixture
def setup_moviesyms_diary(tmp_output):
    metadata_dir = pathlib.Path("tests/data")
    diary_path = pathlib.Path("tests/data/diary.csv")
    m = Moviesyms(metadata_dir, tmp_output, diary_path)
    return m


@pytest.fixture
def setup_moviesyms_emptydiary(tmp_output):
    metadata_dir = pathlib.Path("tests/data")
    diary_path = pathlib.Path("tests/data/diary_empty.csv")
    m = Moviesyms(metadata_dir, tmp_output, diary_path)
    return m


def test_init_nodiary(setup_moviesyms):
    m = setup_moviesyms
    exp_path = pathlib.Path("/movie_root_dir/1999 The Matrix")
    assert set(m.mapping["disk_path"]) == set([exp_path])
    assert set(m.mapping["name"]) == set(["1999 The Matrix"])


def test_init_diary(setup_moviesyms_diary):
    m = setup_moviesyms_diary
    exp_path = pathlib.Path("/movie_root_dir/1999 The Matrix")
    assert set(m.mapping_diary["disk_path"]) == set([exp_path])
    assert set(m.mapping_diary.columns) == set(
        [
            "last_seen_in",
            "disk_path",
            "letterboxd_uri",
            "rating",
            "watched_date",
            "watched",
            "date",
            "tags",
            "tmdb_id",
            "rewatch",
        ]
    )

    # @pytest.skip("TBD: show guessing different merging styles", allow_module_level=False)
    # def test_guess_style():
    #     pass

    # @pytest.skip("TBD: append diary but no matches", allow_module_level=False)
    # def test_guess_style():
    #     pass
    """
    creating with diary,
    then making non-diary calls will break stuff 
    """


def test_non_diary_calls(setup_moviesyms, tmp_output):

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        setup_moviesyms.create_ratings()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == "diary is empty!"

    subdir = tmp_output / "rating" / "4.0"
    assert subdir.exists() is False

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        setup_moviesyms.create_last_seen_in()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == "diary is empty!"

    subdir = tmp_output / "last_seen_in" / "2020"
    assert subdir.exists() is False


def test_runtime(setup_moviesyms, tmp_output):
    setup_moviesyms.create_runtime()
    subdir = tmp_output / "runtime" / "150"
    assert subdir.exists()
    check_for_correct_symlinks_in_subdir(subdir)


def test_decade(setup_moviesyms, tmp_output):
    setup_moviesyms.create_decade()
    subdir = tmp_output / "decade" / "1990"
    assert subdir.exists()
    check_for_correct_symlinks_in_subdir(subdir)


def test_countries(setup_moviesyms, tmp_output):
    setup_moviesyms.create_countries()
    subdir = tmp_output / "countries" / "United States of America"
    assert subdir.exists()
    check_for_correct_symlinks_in_subdir(subdir)


def test_genres(setup_moviesyms, tmp_output):
    setup_moviesyms.create_genres()
    for x in ["Action", "Science Fiction"]:
        subdir = tmp_output / "genres" / x
        assert subdir.exists()
        check_for_correct_symlinks_in_subdir(subdir)


def test_spoken_langs(setup_moviesyms, tmp_output):
    setup_moviesyms.create_spoken_languages()
    subdir = tmp_output / "spoken_languages" / "English"
    assert subdir.exists()
    check_for_correct_symlinks_in_subdir(subdir)


def test_directors(setup_moviesyms, tmp_output):
    setup_moviesyms.create_directors()
    for x in ["Lilly Wachowski", "Lana Wachowski"]:
        subdir = tmp_output / "directors" / x
    assert subdir.exists()
    check_for_correct_symlinks_in_subdir(subdir)


def test_ratings(setup_moviesyms_diary, tmp_output):
    setup_moviesyms_diary.create_ratings()
    subdir = tmp_output / "rating" / "4.0"
    assert subdir.exists()
    check_for_correct_symlinks_in_subdir(subdir)


def test_last_seen_in(setup_moviesyms_diary, tmp_output):
    setup_moviesyms_diary.create_last_seen_in()
    subdir = tmp_output / "last_seen_in" / "2020"
    assert subdir.exists()
    check_for_correct_symlinks_in_subdir(subdir)
