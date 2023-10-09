import logging
import stat
from pathlib import Path
from shutil import rmtree
from subprocess import run
from typing import Optional

import chess

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

WORKING_SPACE_DIR = Path.cwd() / "working"
SOURCE_CODE_DIR = WORKING_SPACE_DIR / "sources"
ENGINE_BIN_DIR = WORKING_SPACE_DIR / "bins"
OPENING_FILE = WORKING_SPACE_DIR / "opening_suite.pgn"
SELECTED_OPENING_SUITE = (
    Path.cwd() / "src" / "opening_suites" / "UHO_2022_8mvs_big_+170_+199.pgn"
)

GIT_CLONE_URL = "https://github.com/Bobingstern/TinyChess"
CMAKE_BUILD_SYSTEM = "Ninja"


def run_cmd(cmd: str, cwd: Optional[Path] = None):
    """
    Run a shell command.

    :param cmd: Command to run.
    :param cwd: Current working directory to set.
    """
    logger.debug(
        f"Running command {cmd}" + f" with cwd {cwd}" if cwd is not None else ""
    )
    run(cmd, shell=True, cwd=cwd)


def delete_dot_git_dir(path: Path):
    """
    Deletes a .git directory.

    :param path: Path to the .git directory.
    """
    logger.debug(f"Deleting git directory {path}")
    for p in path.rglob("*"):
        if p.is_file():
            logger.debug(f"Changing file permission of {p} to S_IWRITE")
            p.chmod(stat.S_IWRITE)
    logger.debug(f"Deleting directory {path}")
    rmtree(path)


def fetch_source_code(commit: str, no_cache: bool = True) -> Path:
    """
    Fetch the source code of the engine and checkout a commit or branch.

    :param commit: Hash or branch or "cwd".
    :param no_cache: Do not cache the source code.
    :return: A pathlib.Path pointing to the source code directory.
    """
    logger.info(f"Fetching source code for engine commit {commit}")
    SOURCE_CODE_DIR.mkdir(parents=True, exist_ok=True)
    engine_source_dir = SOURCE_CODE_DIR / commit
    logger.debug(f"Engine source directory is {engine_source_dir}")

    if engine_source_dir.exists():
        if not no_cache:
            logger.debug(f"Found cached version of source code")
            engine_source_dir = engine_source_dir / "TinyChess"
            logger.debug(f"Attempting pull in order to update branch")
            run_cmd("git pull", engine_source_dir)
            return engine_source_dir
        dot_git_dir = engine_source_dir / "TinyChess" / ".git"
        if dot_git_dir.exists():
            delete_dot_git_dir(dot_git_dir)
        logger.debug(f"Removing {engine_source_dir}")
        rmtree(engine_source_dir)
    logger.debug(f"Creating {engine_source_dir}")
    engine_source_dir.mkdir()

    run_cmd(f"git clone {GIT_CLONE_URL}", engine_source_dir)
    engine_source_dir = engine_source_dir / "TinyChess"
    run_cmd(f"git checkout {commit}", engine_source_dir)

    main_cpp_path = engine_source_dir / "src" / "main.cpp"
    logger.debug(f"main.cpp path is {main_cpp_path}")
    main_cpp_code = main_cpp_path.read_text()
    if "id name TinyChess" not in main_cpp_code:
        logger.warning("Could not change chess engine UCI name!")
    else:
        logger.debug(f"Modifying chess engine UCI name!")
        main_cpp_path.write_text(
            main_cpp_code.replace(
                '"id name TinyChess"', f'"id name TinyChess-{commit}"'
            )
        )

    return engine_source_dir


def compile_cmake_project(
    path: Path, build_type: str = "Debug", no_cache: bool = True
) -> Path:
    """
    Compile a CMake project.

    :param path: The path to the directory with the CMakeLists.txt file.
    :param build_type: Build type. "Debug" or "Release"
    :param no_cache: Do not cache the binary.
    :return: A pathlib.Path pointing to the binary.
    """
    logger.info(f"Compiling CMake project at {path}")

    build_dir = path / "build"
    if build_dir.exists():
        if not no_cache:
            logger.debug(f"Found cached version of binary")
            bin_path = build_dir / "main.exe"
            if bin_path.exists():
                logger.debug(f"Binary path is at {bin_path}")
                return bin_path
            else:
                bin_path = build_dir / "main"
                if bin_path.exists():
                    logger.debug(f"Binary path is at {bin_path}")
                    return bin_path
            logger.debug("Could not find binary in cache, rebuilding!")
        rmtree(build_dir)
    build_dir.mkdir()

    logger.debug(f"Generating build system with type {build_type}")
    run_cmd(
        f'cmake .. -G "{CMAKE_BUILD_SYSTEM}" -D CMAKE_BUILD_TYPE={build_type}',
        build_dir,
    )

    logger.debug(f"Compiling binary")
    run_cmd(f"cmake --build .", build_dir)

    bin_path = build_dir / "main.exe"
    if bin_path.exists():
        logger.debug(f"Binary path is at {bin_path}")
        return bin_path
    else:
        bin_path = build_dir / "main"
        if bin_path.exists():
            logger.debug(f"Binary path is at {bin_path}")
            return bin_path
    raise FileNotFoundError("Could not find binary!")


def run_sprt(
    engine1_bin: Path,
    engine2_bin: Path,
    time_control: str,
    games: str,
    concurrency: str,
    no_book: bool = False,
    save_fens: Optional[Path] = None,
):
    """
    Run a Sequential Probability Ratio Test.

    :param engine1_bin: Path to engine 1 bin.
    :param engine2_bin: Path to engine 2 bin.
    :param time_control: Time control.
    :param games: Game count.
    :param concurrency: Concurrency count.
    :param no_book: Disable the use of an opening book.
    :param save_fens: Save FENs to this location.
    """
    logger.info("Running SPRT" + " with no book" if no_book else "")
    fen_loc = save_fens.expanduser().resolve().with_suffix(".unfixed.fens")
    logger.debug(f"Saving FENs to {fen_loc}")
    assert engine1_bin.parent == engine2_bin.parent
    cwd = engine1_bin.parent
    engine1_cmd = engine1_bin.stem
    engine2_cmd = engine2_bin.stem
    logger.info(f"Starting SPRT between {engine1_cmd} and {engine2_cmd}")
    run_cmd(
        f"cutechess-cli -engine cmd={engine1_cmd} -engine cmd={engine2_cmd} -each "
        f"proto=uci tc={time_control} timemargin=300 -sprt elo0=0 elo1=5 alpha=0.05 "
        f"beta=0.05 -games {games} -concurrency {concurrency}"
        + (
            ""
            if no_book
            else f" -openings file={OPENING_FILE.expanduser().resolve()} format=pgn"
        )
        + ("" if save_fens is None else f" -epdout {fen_loc}"),
        cwd,
    )


def fix_fens(fen_loc: Path) -> Path:
    """
    Fix FENs to include brackets of result. [1.0], [0.5], [0.0]

    :param fen_loc: Location of FENs.
    :return: Location of fixed FENs.
    """
    logger.info(f"Fixing FENs at {fen_loc}")
    new_fen_loc = fen_loc.with_stem(fen_loc.stem.replace(".unfixed", ""))
    logger.info(f"New FEN path is {new_fen_loc}")
    with fen_loc.open(mode="rt") as unfixed_fens_file, new_fen_loc.open(
        mode="wt"
    ) as fixed_fens_file:
        for unfixed_fen in unfixed_fens_file:
            board = chess.Board(unfixed_fen)
            outcome = board.outcome()
            fixed_fen = f"{unfixed_fen.strip()}"
            if outcome is None:
                fixed_fen += " [0.5]\n"
            elif outcome.termination == chess.Termination.CHECKMATE:
                if outcome.winner == chess.WHITE:
                    fixed_fen += " [1.0]\n"
                else:
                    fixed_fen += " [0.0]\n"
            fixed_fens_file.write(fixed_fen)
    return new_fen_loc
