# Meerkat Backend

## Installation

### Manual Setup
- Install Python 3.9+
- Create virtual environment: `python3 -m venv venv`
- Activate environment: `source venv/bin/activate`
- Install Poetry: `pip install poetry`
- Install dependencies: `poetry install --no-root`
- Install pre-commit hooks: `pre-commit install`

### Automated Setup
```bash
chmod +x install.sh
./install.sh
```

## Configuration
- Copy `app/config/resource/env.yaml` to `env_dev_fest_alps_test.yaml`
- Add Firebase credentials to `app/config/resource/firebase-adminsdk.json`

## Run

### Local
```bash
source venv/bin/activate
python -m app.main
```

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up
```

### Docker Development (with live reload)
```bash
docker-compose -f docker-compose.dev.yml up
```

## Development
- Linting: `poetry run ruff check .`
- Type checking: `poetry run pyright .`
- Tests: `poetry run pytest`
- Pre-commit runs automatically on commit