import logging
import shutil
from argparse import ArgumentParser
from pathlib import Path

from tinychess_test import (
    ENGINE_BIN_DIR,
    OPENING_FILE,
    SELECTED_OPENING_SUITE,
    fix_fens,
    run_sprt,
)
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

parser = ArgumentParser(
    prog="TinyChessTest",
    description="A program for tournament setup for elo testing the TinyChess engine.",
)
parser.add_argument(
    "--engine-1-commit",
    "-e1c",
    metavar="COMMIT",
    type=str,
    required=True,
    help="TinyChess commit for engine 1. Is passed to `git checkout`, so it can be a "
    "commit hash or branch.",
)
parser.add_argument(
    "--engine-2-commit",
    "-e2c",
    metavar="COMMIT",
    type=str,
    required=True,
    help="TinyChess commit for engine 2. Is passed to `git checkout`, so it can be a "
    "commit hash or branch.",
)
parser.add_argument(
    "--build-type",
    "-bt",
    choices=("Debug", "Release"),
    default="Debug",
    help="Build target type when compiling the engines. Defaults to Debug.",
)
parser.add_argument(
    "--time-control",
    "-tc",
    metavar="TC",
    type=str,
    default="60+1",
    help="(cutechess-cli tc documentation) Set the time control.  The format is "
    "moves/time+increment, where moves is the number of moves per tc, time is "
    "time per tc (either seconds or minutes:seconds), and increment is the time "
    "increment per move in seconds.  Infinite time control can be set with inf. The "
    "default is 60+1.",
)
parser.add_argument(
    "--games",
    "-g",
    metavar="COUNT",
    type=int,
    default=50,
    help="Number of games. Defaults to 50.",
)
parser.add_argument(
    "--concurrency",
    "-c",
    metavar="COUNT",
    type=int,
    default=1,
    help="Number of concurrent games. Defaults to 1.",
)
parser.add_argument(
    "--no-book", "-nb", action="store_true", help="Disables the use of an opening book."
)
parser.add_argument(
    "--save-fen",
    "-sf",
    metavar="PATH",
    default=None,
    help="Save the FENs of the game to a file path.",
)

args = parser.parse_args()
logger.debug(f"Arguments received: {args}")

save_fen_loc = Path(args.save_fen) if args.save_fen is not None else None
logger.debug(f"Saving FENs to {save_fen_loc.expanduser().resolve()}")

engine1: str = args.engine_1_commit.lower().strip()
engine2: str = args.engine_2_commit.lower().strip()

if engine1 == engine2:
    logger.warning(
        f"Engine 1 {engine1} and engine 2 {engine2} are the same, no elo differences "
        f"expected!"
    )

# engine1_dir = fetch_source_code(engine1)
# engine2_dir = fetch_source_code(engine2)
#
# logger.debug(f"Engine 1 directory is at {engine1_dir}")
# logger.debug(f"Engine 2 directory is at {engine2_dir}")
#
# engine1_bin = compile_cmake_project(engine1_dir, args.build_type)
# engine2_bin = compile_cmake_project(engine2_dir, args.build_type)
engine1_bin = Path(
    r"E:\TinyChessTest\working\sources\5747a4eb4c0834b72ad39381c0f2074a1601d52e\TinyChess\build\main.exe"
)
engine2_bin = Path(r"E:\TinyChessTest\working\sources\main\TinyChess\build\main.exe")

logger.debug(f"Engine 1 binary is at {engine1_bin}")
logger.debug(f"Engine 2 binary is at {engine2_bin}")

logger.info("Copying binaries")
ENGINE_BIN_DIR.mkdir(exist_ok=True)
engine1_new_bin = ENGINE_BIN_DIR / f"tinychess-{engine1}.exe"
engine2_new_bin = ENGINE_BIN_DIR / f"tinychess-{engine2}.exe"
if engine1_new_bin.exists():
    logger.debug(f"Deleting {engine1_new_bin}")
    engine1_new_bin.unlink()
engine1_new_bin.touch()
if engine2_new_bin.exists():
    logger.debug(f"Deleting {engine2_new_bin}")
    engine2_new_bin.unlink()
engine2_new_bin.touch()
logger.debug(f"Copying {engine1_bin} to {engine1_new_bin}")
shutil.copy(engine1_bin, engine1_new_bin)
logger.debug(f"Copying {engine2_bin} to {engine2_new_bin}")
shutil.copy(engine2_bin, engine2_new_bin)

logger.info(f"Copying opening suite from {SELECTED_OPENING_SUITE}")
OPENING_FILE.touch()
shutil.copy(SELECTED_OPENING_SUITE, OPENING_FILE)

run_sprt(
    engine1_new_bin,
    engine2_new_bin,
    args.time_control,
    args.games,
    args.concurrency,
    args.no_book,
    save_fen_loc,
)

if save_fen_loc is not None:
    logger.debug(f"Fixing FENs")
    unfixed_fens_loc = save_fen_loc.with_suffix(".unfixed.fens")
    fixed_fens_loc = fix_fens(unfixed_fens_loc)
    unfixed_fens_loc.unlink()
    logger.info(f"Fixed FENs at {fixed_fens_loc}")
