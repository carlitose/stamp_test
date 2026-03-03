## ADDED Requirements

### Requirement: Ruff configuration
The project SHALL include Ruff configuration in `pyproject.toml` with:
- Target Python version: 3.12
- Line length: 120
- Enabled rule sets: E (pycodestyle errors), F (pyflakes), I (isort), UP (pyupgrade)
- `src/lambda/` and `tests/` as source directories

#### Scenario: Ruff runs without configuration errors
- **WHEN** a developer runs `ruff check .`
- **THEN** Ruff SHALL use the configured rules and report any violations

#### Scenario: Ruff format is consistent
- **WHEN** a developer runs `ruff format .`
- **THEN** all Python files SHALL be formatted with 120-char line length

### Requirement: Pytest configuration
The project SHALL include pytest configuration in `pyproject.toml` with:
- Test discovery path: `tests/`
- Verbose output enabled by default

#### Scenario: Pytest discovers tests
- **WHEN** a developer runs `pytest`
- **THEN** pytest SHALL discover and run tests from the `tests/` directory
