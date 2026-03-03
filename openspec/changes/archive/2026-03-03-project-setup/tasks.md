## 1. Project Scaffolding

- [x] 1.1 Create directory structure: `src/lambda/`, `tests/`, `terraform/`, `.github/workflows/`
- [x] 1.2 Add `__init__.py` files to `src/lambda/` and `tests/`
- [x] 1.3 Create `.gitignore` with Python, Terraform, IDE, OS, and env exclusions
- [x] 1.4 Create `.python-version` file with `3.12`
- [x] 1.5 Create `sample.csv` with test data (3 numeric cols + email, at least 3 rows)

## 2. Dependency Management

- [x] 2.1 Create `requirements.txt` with `boto3>=1.34,<2.0`
- [x] 2.2 Create `requirements-dev.txt` with `-r requirements.txt`, pytest, moto[s3,ses], ruff

## 3. Dev Tooling Configuration

- [x] 3.1 Create `pyproject.toml` with Ruff config (target py312, line-length 120, rules E/F/I/UP)
- [x] 3.2 Add pytest config to `pyproject.toml` (testpaths = tests/, verbose)

## 4. Verification

- [x] 4.1 Install dependencies in a virtualenv and verify all packages install cleanly
- [x] 4.2 Run `ruff check .` and verify no configuration errors
- [x] 4.3 Run `pytest` and verify it discovers the tests directory (0 tests collected is OK)
