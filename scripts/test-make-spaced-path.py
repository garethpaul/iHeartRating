#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHILD_MARKER = "IHEARTRATING_MAKE_SPACE_CHILD"


def run_make(make, arguments, caller, environment):
    return subprocess.run(
        [make, *arguments],
        cwd=caller,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )


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
        make = environment.get("IHEARTRATING_MAKE", "make")
        repository_makefile = str(copied / "Makefile")
        subprocess.run(
            [make, "-f", repository_makefile, "check"],
            cwd=caller,
            env=environment,
            check=True,
            timeout=180,
        )

        extra_makefile = root / "extra.mk"
        extra_makefile.write_text(".PHONY: extra\nextra:\n\t@:\n", encoding="utf-8")
        replacement_makefile = root / "replacement.mk"
        replacement_makefile.write_text(
            ".PHONY: check xcode-test\ncheck xcode-test:\n\t@echo BYPASSED\n",
            encoding="utf-8",
        )

        preload_environment = environment.copy()
        preload_environment["MAKEFILES"] = str(extra_makefile)
        preload = run_make(make, ["-f", repository_makefile, "check"], caller, preload_environment)
        if preload.returncode == 0 or "MAKEFILES must be empty" not in preload.stderr:
            raise RuntimeError("MAKEFILES preload must fail closed")

        overridden = run_make(make, ["-f", repository_makefile, "MAKEFILE_LIST=untrusted", "check"], caller, environment)
        if overridden.returncode == 0 or "MAKEFILE_LIST must not be overridden" not in overridden.stderr:
            raise RuntimeError("MAKEFILE_LIST override must fail closed")

        for arguments in (
            ["-f", str(extra_makefile), "-f", repository_makefile, "check"],
            ["-f", repository_makefile, "-f", str(extra_makefile), "check"],
        ):
            multiple = run_make(make, arguments, caller, environment)
            if multiple.returncode == 0 or "repository Makefile must be loaded alone" not in multiple.stderr:
                raise RuntimeError("multiple loaded Makefiles must fail closed")

        for target in ("check", "xcode-test"):
            replacement = run_make(
                make,
                ["-f", repository_makefile, "-f", str(replacement_makefile), target],
                caller,
                environment,
            )
            if replacement.returncode == 0 or "BYPASSED" in replacement.stdout:
                raise RuntimeError(f"later recipes must not replace repository verification: {target}")


if __name__ == "__main__":
    main()
