#!/usr/bin/env python3
import os
import subprocess
import sys


def main() -> None:
    """Setup the development environment"""
    print("🐾 Setting up Meerkat Backend...")

    try:
        # Create venv if it doesn't exist
        if not os.path.exists("venv"):
            print("📦 Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

        # Install dependencies
        print("⚡ Installing dependencies...")
        subprocess.run(["poetry", "install", "--no-root"], check=True)

        # Copy config if needed
        config_src = "app/config/resource/env.yaml"
        config_dst = "app/config/resource/env_dev_fest_alps_test.yaml"
        if not os.path.exists(config_dst) and os.path.exists(config_src):
            print("📝 Creating config file...")
            subprocess.run(["cp", config_src, config_dst], check=True)

        # Install pre-commit
        print("🪝 Installing pre-commit hooks...")
        subprocess.run(["poetry", "run", "pre-commit", "install"], check=True)

        print("✅ Setup complete!")
        print(
            "Next: Add Firebase credentials to app/config/resource/firebase-adminsdk.json"
        )

    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
