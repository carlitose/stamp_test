## ADDED Requirements

### Requirement: Project directory structure
The project SHALL have the following directory structure:
- `src/lambda/` — Lambda function source code
- `tests/` — Test files
- `terraform/` — Terraform configuration (empty, scaffolded)
- `.github/workflows/` — GitHub Actions workflows (empty, scaffolded)

Each Python package directory (`src/lambda/`, `tests/`) SHALL contain an `__init__.py` file.

#### Scenario: Directory structure exists after setup
- **WHEN** the project setup is complete
- **THEN** directories `src/lambda/`, `tests/`, `terraform/`, `.github/workflows/` SHALL exist
- **THEN** `src/lambda/__init__.py` and `tests/__init__.py` SHALL exist

### Requirement: Git ignore configuration
The project SHALL include a `.gitignore` file that excludes:
- Python artifacts: `__pycache__/`, `*.pyc`, `*.pyo`, `*.egg-info/`, `dist/`, `build/`
- Virtual environments: `venv/`, `.venv/`, `env/`
- IDE files: `.idea/`, `.vscode/`, `*.swp`
- Environment files: `.env`, `.env.local`
- Terraform state and artifacts: `.terraform/`, `*.tfstate`, `*.tfstate.backup`, `.terraform.lock.hcl`
- OS files: `.DS_Store`, `Thumbs.db`

#### Scenario: Gitignore excludes standard artifacts
- **WHEN** a developer creates a virtual environment or generates Python bytecode
- **THEN** those files SHALL NOT appear in `git status`

### Requirement: Python version pinning
The project SHALL include a `.python-version` file specifying `3.12`.

#### Scenario: Python version is pinned
- **WHEN** a developer uses pyenv or a similar tool
- **THEN** the tool SHALL automatically select Python 3.12

### Requirement: Sample CSV file
The project SHALL include a `sample.csv` file with test data matching the spec format (3 numeric columns + 1 email column), containing at least 3 rows with varied data (positive, negative, decimal values).

#### Scenario: Sample CSV is valid
- **WHEN** the sample CSV is used for manual testing
- **THEN** it SHALL contain rows with 3 numeric values and a valid email address per row
