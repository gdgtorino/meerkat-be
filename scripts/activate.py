#!/usr/bin/env python3
import os
import sys


def main() -> None:
    """Show how to activate the virtual environment"""
    venv_path = os.path.join(os.getcwd(), "venv")

    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found. Run 'poetry run setup' first.")
        sys.exit(1)

    activate_script = os.path.join(venv_path, "bin", "activate")

    print("To activate the virtual environment, run:")
    print(f"source {activate_script}")
    print("")
    print("Or use poetry commands directly:")
    print("poetry run dev      # Start development server")
    print("poetry run test     # Run tests")
    print("poetry run lint     # Run linting")
    print("poetry run format   # Format code")


if __name__ == "__main__":
    main()
