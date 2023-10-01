# TinyChessTest

A program for tournament setup for elo testing the
[TinyChess](https://github.com/Bobingstern/TinyChess) engine.

## Install

1. Have Python, Ninja, CMake, and cutechess-cli installed and in PATH. (tested
   only on Python 3.11)
2. Clone this repo.
3. Create virtual environment if desired.
4. Install requirements in [`requirements.txt`](requirements.txt).

## Run

Run [`src/main.py`](src/main.py).

Example command to
test [`1870905aca990956a53c5cbe8dfa6c2d786ea57e`](https://github.com/Bobingstern/TinyChess/commit/1870905aca990956a53c5cbe8dfa6c2d786ea57e)
against the main branch.

```commandline
python src/main.py --engine-1-commit 1870905aca990956a53c5cbe8dfa6c2d786ea57e --engine-2-commit main
```

### Help

```commandline
usage: TinyChessTest [-h] --engine-1-commit COMMIT --engine-2-commit COMMIT
                     [--no-cache] [--time-control TC] [--games COUNT]
                     [--concurrency COUNT]

A program for tournament setup for elo testing the TinyChess engine.

options:
  -h, --help            show this help message and exit
  --engine-1-commit COMMIT, -e1c COMMIT
                        TinyChess commit for engine 1. Is passed to `git
                        checkout`, so it can be a commit hash or branch.
  --engine-2-commit COMMIT, -e2c COMMIT
                        TinyChess commit for engine 2. Is passed to `git
                        checkout`, so it can be a commit hash or branch.
  --no-cache            Whether to not use the cache.
  --time-control TC, -tc TC
                        (cutechess-cli tc documentation) Set the time control.
                        The format is moves/time+increment, where moves is the
                        number of moves per tc, time is time per tc (either
                        seconds or minutes:seconds), and increment is the time
                        increment per move in seconds. Infinite time control
                        can be set with inf. The default is 60+1.
  --games COUNT, -g COUNT
                        Number of games. Defaults to 50.
  --concurrency COUNT, -c COUNT
                        Number of concurrent games. Defaults to 5.
```
