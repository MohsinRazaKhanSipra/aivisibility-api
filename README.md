# AI Visibility API

AI Visibility API is a Flask-based backend template for managing AI-related profiles, queries, recommendations, and pipeline orchestration. It includes a modular architecture with:

- `app/api/` for request handlers and blueprint registration
- `app/models/` for SQLAlchemy data models
- `app/agents/` for agent logic such as discovery, scoring, and recommendation
- `app/services/` for pipeline orchestration and business workflows
- `app/utils/` for reusable utilities like scoring functions

## Features

- Flask application factory pattern
- Blueprint-based API structure
- SQLAlchemy + Flask-Migrate support
- Modular agent and pipeline service design
- Test scaffolding with `tests/`

## Requirements

- Python 3.10+ (recommended)
- `pip`

## Setup

1. Create and activate a virtual environment:

   On Windows:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS/Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables:

   On Windows:
   ```powershell
   copy .env.example .env
   ```

   On macOS/Linux:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` values as needed.

## Running the app

Start the Flask application with:

```bash
python run.py
```

By default, the app will run on `http://127.0.0.1:5000`.


## Testing

```bash
cd tests
```

```bash
python .\test_api_script.py
```

## Project structure

- `app/`
  - `__init__.py`: app factory and blueprint registration
  - `extensions.py`: database and migration extension setup
  - `models/`: model definitions
  - `agents/`: agent service classes
  - `services/`: pipeline orchestration logic
  - `api/`: API blueprints
  - `utils/`: helper utilities
- `migrations/`: database migration files
- `tests/`: test file
- `.env.example`: environment variable template
- `requirements.txt`: Python dependency list
- `run.py`: app entry point


