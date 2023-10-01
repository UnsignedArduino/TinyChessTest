import logging
from argparse import ArgumentParser
from pathlib import Path

from tinychesstest import compile_cmake_project
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
    r"E:\TinyChessTest\working\sources\1870905aca990956a53c5cbe8dfa6c2d786ea57e\TinyChess"
)
engine2_dir = Path(r"E:\TinyChessTest\working\sources\main\TinyChess")

logger.debug(f"Engine 1 directory is at {engine1_dir}")
logger.debug(f"Engine 2 directory is at {engine2_dir}")

engine1_bin = compile_cmake_project(engine1_dir)
engine2_bin = compile_cmake_project(engine2_dir)

logger.debug(f"Engine 1 binary is at {engine1_bin}")
logger.debug(f"Engine 2 binary is at {engine2_bin}")
