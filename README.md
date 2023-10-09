# TinyChessTest

A program for tournament setup for elo testing the
[TinyChess](https://github.com/Bobingstern/TinyChess) engine.

## Install

1. Have Python, MinGW, Make, CMake, and cutechess-cli installed and in PATH.
   (tested only on Python 3.11)
2. Clone this repo.
3. Create virtual environment if desired.
4. Install requirements in [`requirements.txt`](requirements.txt).

## Run

Run [`src/main.py`](src/main.py).

Example command to test
[`5747a4eb4c0834b72ad39381c0f2074a1601d52e`](https://github.com/Bobingstern/TinyChess/commit/5747a4eb4c0834b72ad39381c0f2074a1601d52e)
against the main branch.

```commandline
python src/main.py --engine-1-commit 5747a4eb4c0834b72ad39381c0f2074a1601d52e --engine-2-commit main
```

Example command to test
[`5747a4eb4c0834b72ad39381c0f2074a1601d52e`](https://github.com/Bobingstern/TinyChess/commit/5747a4eb4c0834b72ad39381c0f2074a1601d52e)
against the main branch with a time control of 5+0.01 and 1000 games with
concurrency of 5 and save FENs to `output.fens`.

```commandline
python src/main.py --engine-1-commit 5747a4eb4c0834b72ad39381c0f2074a1601d52e --engine-2-commit main --concurrency 5 --time-control 5+0.01 --games 1000 --save-fens output.fens
```

### Help

```commandline
usage: TinyChessTest [-h] --engine-1-commit COMMIT --engine-2-commit COMMIT
                     [--build-type {Debug,Release}] [--time-control TC]
                     [--games COUNT] [--concurrency COUNT] [--no-book]
                     [--save-fen PATH]

A program for tournament setup for elo testing the TinyChess engine.

options:
  -h, --help            show this help message and exit
  --engine-1-commit COMMIT, -e1c COMMIT
                        TinyChess commit for engine 1. Is passed to `git
                        checkout`, so it can be a commit hash or branch.
  --engine-2-commit COMMIT, -e2c COMMIT
                        TinyChess commit for engine 2. Is passed to `git
                        checkout`, so it can be a commit hash or branch.
  --build-type {Debug,Release}, -bt {Debug,Release}
                        Build target type when compiling the engines. Defaults
                        to Debug.
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
                        Number of concurrent games. Defaults to 1.
  --no-book, -nb        Disables the use of an opening book.
  --save-fen PATH, -sf PATH
                        Save the FENs of the game to a file path.
```
