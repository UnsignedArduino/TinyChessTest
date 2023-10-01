import logging
import shutil
from argparse import ArgumentParser
from pathlib import Path

from silver_opening_suite import get_silver_opening_suite_pgn
from tinychess_test import ENGINE_BIN_DIR, SILVER_SUITE_FILE
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

parser = ArgumentParser(
    prog="TinyChessTest",
    description="A program for tournament setup for elo testing the TinyChess engine.",
)
parser.add_argument(
    "--engine-1-commit",
    "--e1c",
    metavar="COMMIT",
    type=str,
    required=True,
    help="TinyChess commit for engine 1. Is passed to `git checkout`, so it can be a "
    "commit hash or branch.",
)
parser.add_argument(
    "--engine-2-commit",
    "--e2c",
    metavar="COMMIT",
    type=str,
    required=True,
    help="TinyChess commit for engine 2. Is passed to `git checkout`, so it can be a "
    "commit hash or branch.",
)

args = parser.parse_args()
logger.debug(f"Arguments received: {args}")

engine1: str = args.engine_1_commit.lower().strip()
engine2: str = args.engine_2_commit.lower().strip()

if engine1 == engine2:
    logger.warning(
        f"Engine 1 {engine1} and engine 2 {engine2} are the same, no elo differences "
        f"expected!"
    )

# engine1_dir, engine2_dir = fetch_source_code(engine1, engine2)
# For testing
engine1_dir = Path(
    r"E:\TinyChessTest\working\sources\1870905aca990956a53c5cbe8dfa6c2d786ea57e"
    r"\TinyChess"
)
engine2_dir = Path(r"E:\TinyChessTest\working\sources\main\TinyChess")

logger.debug(f"Engine 1 directory is at {engine1_dir}")
logger.debug(f"Engine 2 directory is at {engine2_dir}")

# engine1_bin = compile_cmake_project(engine1_dir)
# engine2_bin = compile_cmake_project(engine2_dir)
# For testing
engine1_bin = Path(
    r"E:\TinyChessTest\working\sources\1870905aca990956a53c5cbe8dfa6c2d786ea57e"
    r"\TinyChess\build\main.exe"
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

logger.info(f"Copying Silver opening suite")
SILVER_SUITE_FILE.write_text(get_silver_opening_suite_pgn())
