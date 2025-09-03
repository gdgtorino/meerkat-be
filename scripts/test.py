#!/usr/bin/env python3
import subprocess
import sys


def main() -> None:
    """Run pytest tests"""
    result = subprocess.run(["pytest"], cwd=".")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
