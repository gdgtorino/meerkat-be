#!/usr/bin/env python3
import subprocess
import sys


def main() -> None:
    """Run ruff formatting"""
    result = subprocess.run(["ruff", "format", "."], cwd=".")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
