## Context

This is a greenfield project — no existing code, no existing infrastructure. We need to establish the local development environment and project scaffolding before any Lambda code or Terraform can be written.

The target runtime is AWS Lambda with Python 3.12. All development tooling (linting, testing, mocking) must work locally without AWS credentials.

## Goals / Non-Goals

**Goals:**
- Reproducible local setup: any developer can clone and be productive in minutes
- Clear separation between runtime and dev dependencies
- Linting and formatting enforced via Ruff from day one
- Testing foundation with pytest and moto for AWS mocking
- Directory structure matching the spec's project layout

**Non-Goals:**
- Writing any application code (handler, services, etc.) — that's `core-lambda`
- Terraform configuration — that's `infrastructure`
- CI/CD pipeline — that's `cicd-and-docs`
- Docker or containerized development
- Pre-commit hooks (can be added later if needed)

## Decisions

### 1. Dependency management: requirements.txt (not Poetry/Pipenv)

**Decision**: Use plain `requirements.txt` + `requirements-dev.txt`.

**Rationale**: Lambda deployment packages work best with pip + requirements.txt. Poetry/Pipenv add complexity with no benefit here — the project has 1 runtime dependency (boto3). Keeps Terraform Lambda packaging simple.

**Alternatives considered**:
- Poetry: Overkill for a project with minimal dependencies, adds lock file complexity
- Pipenv: Less common in Lambda workflows, similar overhead

### 2. Linting: Ruff (not flake8+black)

**Decision**: Ruff as the single tool for linting and formatting.

**Rationale**: Ruff replaces flake8, black, isort, and pyupgrade in one tool. Faster, simpler configuration via `pyproject.toml`. One tool to run, one config to maintain.

### 3. Testing: pytest + moto (not localstack)

**Decision**: Use moto to mock AWS services (S3, SES) in tests.

**Rationale**: moto is lightweight, runs in-process, no Docker needed. Perfect for unit-testing Lambda functions that interact with S3 and SES. Localstack would be overkill for this scope.

### 4. Project root: flat (not monorepo)

**Decision**: All project files at repository root, Lambda code in `src/lambda/`.

**Rationale**: Matches the project spec. Single Lambda function, single concern — no need for monorepo tooling.

## Risks / Trade-offs

- **[boto3 version pinning]** → Pin to a compatible version range. Lambda runtime includes boto3, but moto tests need a matching version. Use `boto3>=1.34,<2.0`.
- **[moto coverage]** → moto covers S3 and SES well, but edge cases (SES sandbox behavior) may not be perfectly simulated. Accepted trade-off for unit test speed.
- **[No pre-commit hooks]** → Developers must remember to run ruff manually. Mitigated by CI/CD linting in the `cicd-and-docs` change.
