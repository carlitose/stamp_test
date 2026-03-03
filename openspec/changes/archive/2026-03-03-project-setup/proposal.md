## Why

The CSV Processor Pipeline needs a properly initialized project structure before any application code can be written. Without a consistent local development environment (Python 3.12, virtual environment, dependencies, linting, testing tools), implementation would be ad-hoc and hard to reproduce. This is the foundation that every subsequent change depends on.

## What Changes

- Create the full project directory structure (`src/lambda/`, `tests/`, `terraform/`, `.github/workflows/`)
- Add `.gitignore` with standard Python + Terraform exclusions
- Add `requirements.txt` with runtime dependency (boto3)
- Add `requirements-dev.txt` with development dependencies (pytest, moto, ruff)
- Pin Python 3.12 via `.python-version`
- Add `sample.csv` for manual testing
- Add `pyproject.toml` with Ruff configuration

## Capabilities

### New Capabilities
- `project-scaffolding`: Directory structure, .gitignore, Python version pinning, and sample data
- `dependency-management`: Runtime and dev dependency files, virtual environment setup
- `dev-tooling`: Ruff linting configuration and pytest setup

### Modified Capabilities
<!-- None — this is a greenfield project -->

## Impact

- **Files**: New project scaffolding files at repository root
- **Dependencies**: boto3 (runtime), pytest, moto[ses,s3], ruff (dev)
- **Systems**: Local development environment (Python 3.12 + virtualenv)
- **Downstream**: Every subsequent change (core-lambda, infrastructure, cicd) depends on this setup being in place
