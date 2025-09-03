#!/usr/bin/env python3
import subprocess
import sys


def main() -> None:
    """Run ruff linting"""
    result = subprocess.run(["ruff", "check", "."], cwd=".")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
