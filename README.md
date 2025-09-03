# Meerkat Backend

## Installation

### Manual Setup

- Install Python 3.9+
- Create virtual environment: `python3 -m venv venv`
- Activate environment: `source venv/bin/activate`
- Install Poetry: `pip install poetry`
- Install dependencies: `poetry install --no-root`
- Install pre-commit hooks: `pre-commit install`

### Automated Setup (Shell Script)
```bash
chmod +x install.sh
./install.sh
```

### Automated Setup (Poetry Script)
```bash
pip install poetry
poetry run setup
```

## Configuration

- Copy `app/config/resource/env.yaml` to `env_dev_fest_alps_test.yaml`
- Add Firebase credentials to `app/config/resource/firebase-adminsdk.json`

## Run

### Local
```bash
# Option 1: Manual activation
source venv/bin/activate
python -m app.main

# Option 2: Poetry script
poetry run dev
```

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up
```

### Docker Development (with live reload)

```bash
docker-compose -f docker-compose.yml up
```

## Development

### Poetry Scripts (npm-style)
```bash
poetry run setup        # Initialize repo with venv, deps, pre-commit
poetry run activate     # Show how to activate venv
poetry run lint         # Run ruff linting
poetry run format       # Run ruff formatting
poetry run type-check   # Run pyright type checking
poetry run test         # Run pytest
poetry run dev          # Start development server with reload
```

### Manual Commands
```bash
poetry run ruff check .
poetry run pyright .
poetry run pytest
```

- Pre-commit runs automatically on commit

