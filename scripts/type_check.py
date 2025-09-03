#!/usr/bin/env python3
import subprocess
import sys


def main() -> None:
    """Run pyright type checking"""
    result = subprocess.run(["pyright", "."], cwd=".")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
