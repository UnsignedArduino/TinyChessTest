import logging
import stat
from pathlib import Path
from shutil import rmtree
from subprocess import run
from typing import Optional

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

WORKING_SPACE_DIR = Path.cwd() / "working"
SOURCE_CODE_DIR = WORKING_SPACE_DIR / "sources"

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


def fetch_source_code(engine1: str, engine2: str) -> tuple[Path, Path]:
    """
    Fetch the source code of both engine commits.

    :param engine1: Hash or branch or "cwd"
    :param engine2: Hash or branch or "cwd"
    :return: A tuple of two pathlib.Path pointing to the source code directories.
    """
    logger.info(f"Fetching source code for engine 1 ({engine1}) and 2 ({engine2})")
    SOURCE_CODE_DIR.mkdir(parents=True, exist_ok=True)
    engine1_source_dir = SOURCE_CODE_DIR / engine1
    engine2_source_dir = SOURCE_CODE_DIR / engine2
    logger.debug(f"Engine 1 source directory is {engine1_source_dir}")
    logger.debug(f"Engine 2 source directory is {engine2_source_dir}")

    for dir_to_create in (engine1_source_dir, engine2_source_dir):
        if dir_to_create.exists():
            dot_git_dir = dir_to_create / "TinyChess" / ".git"
            if dot_git_dir.exists():
                delete_dot_git_dir(dot_git_dir)
            logger.debug(f"Removing {dir_to_create}")
            rmtree(dir_to_create)
        logger.debug(f"Creating {dir_to_create}")
        dir_to_create.mkdir()

    run_cmd(f"git clone {GIT_CLONE_URL}", engine1_source_dir)
    engine1_source_dir = engine1_source_dir / "TinyChess"
    run_cmd(f"git checkout {engine1}", engine1_source_dir)

    run_cmd(f"git clone {GIT_CLONE_URL}", engine2_source_dir)
    engine2_source_dir = engine2_source_dir / "TinyChess"
    run_cmd(f"git checkout {engine2}", engine2_source_dir)

    return engine1_source_dir, engine2_source_dir


def compile_cmake_project(path: Path) -> Path:
    """
    Compile a CMake project.

    :param path: The path to the directory with the CMakeLists.txt file.
    :return: A pathlib.Path pointing to the binary.
    """
    logger.info(f"Compiling CMake project at {path}")

    build_dir = path / "build"
    if build_dir.exists():
        rmtree(build_dir)
    build_dir.mkdir()

    logger.debug(f"Generating build system")
    run_cmd(f'cmake .. -G "{CMAKE_BUILD_SYSTEM}"', build_dir)

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
