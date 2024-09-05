# Terraform Jamf Pro Configuration Repository

This repository contains Terraform configurations for managing resources in Jamf Pro across multiple environments using the Jamf Pro Terraform provider. The workflows defined here automate the planning and application of Terraform configurations to your Jamf Pro environments, ensuring that your Jamf Pro settings are version-controlled and consistently applied.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Environment Setup](#environment-setup)
- [Workflow Overview](#workflow-overview)
- [Branching Strategy](#branching-strategy)
- [Drift Detection and Correction](#drift-detection-and-correction)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following prerequisites in place:

- **Jamf Pro Client Credentials**: A Jamf Pro client id and secret with appropriate API access is required. [Client Credentials](https://developer.jamf.com/jamf-pro/docs/client-credentials).
- **Terraform Cloud**: An account on Terraform Cloud for managing Terraform state and running Terraform in a consistent environment. [Sign up for Terraform Cloud](https://app.terraform.io/signup/account).
- **GitHub Account**: A GitHub account for storing this repository and using GitHub Actions for automation. [Sign up for GitHub](https://github.com/join).
- **Fork this repository**: Start by forking this repository into your GitHub account to make changes. You can fork the repository by clicking the "Fork" button at the top right corner of the repository page. Ensure that you unselect `Copy the sandbox branch only` so that all branches are copied to your forked repository.

## Repository Structure

```
.
├── .github
│   └── workflows
│       ├── 00-hotfix.yml
│       ├── 01-terraform-plan-sandbox.yml
│       ├── 02-terraform-apply-sandbox.yml
│       ├── 03-release-and-plan-staging.yml
│       ├── 04-terraform-apply-staging.yml
│       ├── 05-release-and-plan-production.yml
│       ├── 06-terraform-apply-production.yml
│       ├── branch-cleanup.yml
│       ├── create-pr.yml
│       ├── create-version-and-release.yml
│       ├── drift.yml
│       ├── lint.yml
│       ├── send-notification.yml
│       ├── terraform-apply.yml
│       ├── terraform-plan.yml
│       └── update-release.yml
├── workload
│   ├── scripts
│   │   ├── hash_generator.py
│   │   └── version_determinator.py
│   └── terraform
│       └── jamfpro
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
├── README.md
└── .gitignore
```

## Environment Setup

This project supports three environments:

1. Sandbox
2. Staging
3. Production

Each environment has its own Terraform Cloud workspace:

- `terraform-jamfpro-sandbox`
- `terraform-jamfpro-staging`
- `terraform-jamfpro-production`

## Workflow Overview

1. Developers create short-lived branches prefixed with:
   - `feat-*`
   - `fix-*`
   - `docs-*`
   - `style-*`
   - `refactor-*`
   - `test-*`
   - `chore-*`
   - `build-*`
   - `ci-*`
   - `perf-*`
   
   This follows the [Conventional Commits](https://sentenz.github.io/convention/convention/conventional-commits/) specification for commit messages. These branches are merged into the `sandbox` branch for testing.

2. Automated Terraform Planning and PR Management:

   Upon pushing changes to branches matching patterns like feat-*, fix-*, ci-*, etc., the `01-terraform-plan-sandbox.yml` workflow is triggered automatically.
   This workflow performs the following actions:
   - Runs a Terraform speculative plan against the Sandbox environment.
   - Automatically creates a new Pull Request (PR) to the sandbox branch if one doesn't exist, or updates an existing PR.
   - Adds or updates a comment in the PR with the results of the Terraform plan, including the number of resources to be added, changed, or destroyed.
   - Provides a link to the full plan details in Terraform Cloud within the PR comment.
   This process ensures that every push to a feature branch is automatically checked, planned, and documented, facilitating easier review and understanding of proposed changes before merging into the sandbox branch.

3. Once all desired changes have been tested, the short-lived branch is PR'd into the sandbox branch.
   Once merged into the sandbox branch, the changes are automatically applied to the Sandbox environment by `02-terraform-apply-sandbox.yml`.

4. Once the changes are applied to the Sandbox environment, promotion to Staging begins:
   - The `03 - release and terraform plan to: staging` workflow is manually triggered from the sandbox branch.
   - This workflow creates a new version and a new release branch (e.g., `release-v1.2.3`).
   - It then generates a Terraform plan for the Staging environment using this release branch.
   - A pull request is created from the release branch to the staging branch, with the plan for review.

5. After the pull request is reviewed and approved:
   - The pull request is merged into the staging branch.
   - This triggers the `04-terraform-apply-staging` workflow.
   - The workflow checks that the merge is from a release branch (starting with `release-v`), then applies the Terraform changes to the Staging environment.
   - After successful apply, the release branch is cleaned up (deleted).

6. The process for promoting to Production follows a similar pattern:
   - A manual trigger of the `05 - release and terraform plan to: production` workflow is done from the staging branch.
   - A new release branch is created for production promotion.
   - After review and approval, the changes are applied to the Production environment.
   - The production release branch is cleaned up after successful apply.
This approach ensures that each promotion to staging or production is associated with a specific release version, allowing for version tracking and potential rollback if needed.

## Branching Strategy

Our branching strategy consists of long-lived branches, short-lived feature branches, and temporary release branches. Here's a detailed breakdown:

| Branch Type | Branch Name | Purpose | Lifecycle |
|-------------|-------------|---------|-----------|
| Long-lived  | `sandbox`   | Represents the sandbox environment. All feature branches are merged here first. | Permanent |
| Long-lived  | `staging`   | Represents the staging environment. Release branches are merged here for testing before production. | Permanent |
| Long-lived  | `production` | Represents the production environment. Final destination for all changes. | Permanent |
| Short-lived | `feat-*`    | For developing new features | Merged to `sandbox` when complete, then deleted |
| Short-lived | `fix-*`     | For fixing bugs | Merged to `sandbox` when complete, then deleted |
| Short-lived | `docs-*`    | For documentation updates | Merged to `sandbox` when complete, then deleted |
| Short-lived | `style-*`   | For code style changes (formatting, missing semi colons, etc.) | Merged to `sandbox` when complete, then deleted |
| Short-lived | `refactor-*`| For code refactoring | Merged to `sandbox` when complete, then deleted |
| Short-lived | `test-*`    | For adding or updating tests | Merged to `sandbox` when complete, then deleted |
| Short-lived | `chore-*`   | For routine tasks or maintenance | Merged to `sandbox` when complete, then deleted |
| Short-lived | `build-*`   | For changes that affect the build system or external dependencies | Merged to `sandbox` when complete, then deleted |
| Short-lived | `ci-*`      | For changes to CI configuration files and scripts | Merged to `sandbox` when complete, then deleted |
| Short-lived | `perf-*`    | For performance improvements | Merged to `sandbox` when complete, then deleted |
| Temporary   | `release-v*` | Created for each release to staging or production | Created during release process, used for final review and applying changes, then deleted after successful apply |

### Branch Flow

```shell
Time ----->

 feat-*  
 fix-*    
 docs-*          release-v1.0.0            release-v1.1.0
 style-*         (sandbox to staging)      (staging to production)
 refactor-*            |                          |
 test-*                |                          |
 ci-*                  |                          |
 chore-*               |                          |
   |                   |                          |
   v                   v                          v
+--------+        +--------+                 +--------+
|        |        |        |                 |        |
| Sandbox|------->| Sandbox|---------------->| Sandbox|  (Default branch)
|        |        |        |                 |        |
+--------+        +--------+                 +--------+
     ^                 | PR                       | PR
     |                 |                          |
     |                 +                          +
     |            +--------+                 +--------+ 
     |            |        |                 |        |
     +------------| Staging|---------------->| Staging|
     |            |        |                 |        |
     |            +--------+                 +--------+
     |                 ^                          | PR
     |                 |                          |
     |                 |                          +
     |                 |                    +----------+
     |                 |                    |          |
     +-----------------+---------------====>|Production|
                       .                    |          |
                       .                    +----------+
                       .
                       +---> Branch deleted after merge

 Legend:
 -----> : Git Flow
 -----+ : Pull Request
 ====> : Hotfix Flow (when needed)
 ...   : Branch deletion
```


### Notes

- Hotfixes may bypass the normal flow in emergencies, but should be backported to ensure all environments stay in sync.
- Release branches (`release-v*`) are temporary and serve as a stable point for final testing and deployment. They are deleted after successful merge and apply.
- Long-lived branches (`sandbox`, `staging`, `production`) should never be deleted and represent the state of each environment.

## Drift Detection and Correction

The `drift-detection-correction.yml` workflow runs nightly to detect and correct any drift in your environments:

- Checks for drift in Sandbox, Staging, and Production environments
- Automatically corrects drift if detected (i.e manual changes made outside of Terraform in the jamf pro gui)
- Sends notifications (configure as needed)

## Getting Started

[Getting Started Guide](./docs/getting-started.md)

## Troubleshooting

- Check GitHub Actions logs for detailed error messages
- Verify Terraform Cloud workspace configurations
- Ensure Jamf Pro API credentials are correct and have necessary permissions

## Contributing

1. Fork the repository
2. Create a new branch with the appropriate prefix
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.