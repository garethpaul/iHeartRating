#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHILD_MARKER = "IHEARTRATING_MAKE_SPACE_CHILD"


def main():
    if os.environ.get(CHILD_MARKER) == "1":
        return

    tracked = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "-z"]
    ).decode().rstrip("\0").split("\0")
    with tempfile.TemporaryDirectory(prefix="iheartrating-make-space-") as temporary:
        root = Path(temporary)
        copied = root / "repository with spaces"
        caller = root / "external caller"
        shutil.copytree(
            ROOT,
            copied,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.pyo"),
        )
        caller.mkdir()
        subprocess.run(["git", "-C", copied, "init", "-q"], check=True)
        subprocess.run(
            ["git", "-C", copied, "add", "-f", "-N", "--", *tracked],
            check=True,
        )
        environment = os.environ.copy()
        environment[CHILD_MARKER] = "1"
        subprocess.run(
            [environment.get("IHEARTRATING_MAKE", "make"), "-f", str(copied / "Makefile"), "check"],
            cwd=caller,
            env=environment,
            check=True,
            timeout=180,
        )


if __name__ == "__main__":
    main()
