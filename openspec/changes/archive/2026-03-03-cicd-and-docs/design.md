## Context

All application code (Lambda) and infrastructure (Terraform) are implemented and committed. The project needs a deployment pipeline and documentation to be complete. The master spec requires GitHub Actions for CI/CD and a README that enables setup in under 15 minutes.

## Goals / Non-Goals

**Goals:**
- GitHub Actions workflow that deploys infrastructure with `terraform apply`
- Manual trigger (`workflow_dispatch`) — no automatic deploys on push
- AWS credentials passed via GitHub Secrets
- README that covers: overview, prerequisites, setup, deployment, testing, architecture
- README enables a new developer to set up everything from scratch

**Non-Goals:**
- Automated tests in CI (can be added later)
- Multiple environment support (dev/staging/prod)
- Terraform plan as PR comment
- Automated rollback
- Detailed API documentation (the code is self-explanatory)

## Decisions

### 1. Workflow trigger: manual only (`workflow_dispatch`)

**Decision**: The deploy workflow uses `workflow_dispatch` for manual triggering.

**Rationale**: The spec allows manual trigger. For a single-developer project, manual deployment is safer and simpler. Avoids accidental deploys on every push.

### 2. Workflow steps: init → plan → apply

**Decision**: Single job with `terraform init`, `terraform plan`, and `terraform apply -auto-approve`.

**Rationale**: Simple linear flow. No approval step needed for a personal project. The plan output is visible in the Actions log for review.

### 3. Secrets: AWS credentials + sender email

**Decision**: Three GitHub Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `SENDER_EMAIL`.

**Rationale**: Standard AWS credential pattern for GitHub Actions. Sender email is also a secret to avoid hardcoding in the workflow.

### 4. README structure: task-oriented

**Decision**: README organized by what you want to do (setup, deploy, test, understand).

**Rationale**: Evaluators want to quickly understand and reproduce. Task-oriented structure is more scannable than a wall of text.

## Risks / Trade-offs

- **[`-auto-approve`]** → No manual confirmation in CI. Acceptable for this project scope. The workflow is manually triggered, so the trigger itself is the approval.
- **[No state locking]** → Local Terraform state means concurrent runs could conflict. Mitigated by manual trigger (one person, one run at a time).
- **[Secrets management]** → AWS credentials in GitHub Secrets is standard but requires trust in GitHub's security. No alternative for GitHub Actions.
