## Why

The Lambda code and Terraform infrastructure are complete, but there's no way to deploy automatically and no documentation for someone setting up the project from scratch. A GitHub Actions workflow enables repeatable deployments, and a comprehensive README makes the project self-contained for evaluators.

## What Changes

- Add `.github/workflows/deploy.yml` — GitHub Actions workflow for Terraform deployment (manual trigger)
- Add `README.md` — complete project documentation with setup instructions, architecture overview, and usage guide

## Capabilities

### New Capabilities
- `github-actions-deploy`: GitHub Actions workflow for automated Terraform deployment with manual trigger
- `project-readme`: Comprehensive README with setup guide, architecture diagram, and testing instructions

### Modified Capabilities
<!-- None -->

## Impact

- **Files**: `.github/workflows/deploy.yml`, `README.md`
- **Dependencies**: GitHub repository with Actions enabled, AWS credentials as GitHub Secrets
- **Systems**: GitHub Actions CI/CD pipeline
- **Downstream**: This is the final change — completes the project
