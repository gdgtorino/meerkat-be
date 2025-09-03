#!/bin/bash
set -e

echo "🐾 Meerkat Backend Setup"

# Check Python 3
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 not found. Please install Python 3.9+"
  exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Poetry
echo "📚 Installing Poetry..."
pip install poetry

# Install dependencies
echo "⚡ Installing dependencies..."
poetry install --no-root

# Copy config file if needed
if [ ! -f "app/config/resource/env_dev_fest_alps_test.yaml" ]; then
  echo "📝 Creating config file..."
  cp app/config/resource/env.yaml app/config/resource/env_dev_fest_alps_test.yaml
fi

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add Firebase credentials to app/config/resource/firebase-adminsdk.json"
echo "2. Run: source venv/bin/activate && python -m app.main"

