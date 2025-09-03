#!/usr/bin/env python3
import subprocess
import sys


def main() -> None:
    """Start development server"""
    result = subprocess.run(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "11111", "--reload"],
        cwd=".",
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
