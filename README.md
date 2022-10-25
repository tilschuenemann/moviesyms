# moviesyms

moviesyms uses [tmdbparser](https://github.com/tilschuenemann/tmdbparser)s movie metadata to generate symlinks across these categories:

- genres
- directors
- production countries.

My movie are all in one folder, every movie has its own subfolder.

```
my_movies/
    1979 Stalker/
    1968 Symbiopsychotaxiplasm/
output_folder/
    (empty)
```

Running the script will yield the following directory structure, where `->` is a symlink.

```
my_movies/
    1979 Stalker/
    1968 Symbiopsychotaxiplasm/
output_folder/
    genres/
        Documentary/
            -> my_movies/1968 Symbiopsychotaxiplasm
        Drama/
            -> my_movies/1979 Stalker
        Science Fiction/
            -> my_movies/1979 Stalker
    production_countries/
        Soviet Union/
            -> my_movies/1979 Stalker
        United States of America/
            -> my_movies/1968 Symbiopsychotaxiplasm
    directors/
        Andrei Tarkovsky
            -> my_movies/1979 Stalker
        William Greaves/
            -> my_movies/1968 Symbiopsychotaxiplasm
```

# Installation

tbd.

# Usage

tbd.

# Background

I often struggle with movie selection - this program reduces the amount of choices,
is a portable, low level solution.
