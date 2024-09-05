# Getting Started

## Tools Install and Install Setup

Before you start working on this project, you'll need to install several tools to ensure your development environment is properly set up.

### 1. Install an IDE (e.g., Visual Studio Code)
You will need an Integrated Development Environment (IDE) to write and manage your code efficiently. We recommend [Visual Studio Code (VSCode)](https://code.visualstudio.com/) because of its flexibility and a wide range of available extensions for Terraform and Git integration.

#### Recommended VSCode Extensions:
- **Terraform**: Provides syntax highlighting, linting, and IntelliSense for Terraform files.
  - [HashiCorp Terraform Extension](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
- **YAML**: Useful for working with GitHub Actions workflows.
  - [YAML Extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
- **GitLens**: Enhances Git capabilities within VSCode, showing Git blame information, commit history, and more.
  - [GitLens Extension](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
- **Prettier - Code Formatter**: Ensures consistent formatting of your code.
  - [Prettier Extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

### 2. Install Git
Git is essential for version control and managing your project’s source code. Install it from the official website based on your operating system:

- [Git for Windows](https://git-scm.com/download/win)
- [Git for macOS](https://git-scm.com/download/mac)
- [Git for Linux](https://git-scm.com/download/linux)

Once Git is installed, you can verify the installation by running the following command in your terminal or command prompt:

```bash
git --version
```

### 3. Set Up Git User Information

After installing Git, you need to configure your user information. This information is used to track who made the changes in the Git commit history.

Run the following commands to set your Git username and email globally (this can be specific to your GitHub account or organization).

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

To verify that the configuration was successful, run:

```bash
git config --global --list
```
### 4. Install Terraform
Terraform is required to manage the infrastructure resources in this project. You can download it from the official Terraform website:

- [Download Terraform](https://www.terraform.io/downloads.html)

After installing Terraform, verify the installation by running the following command:

```bash
terraform --version
```




1. **Create a New Repository**: Start by forking or cloning this repository into your GitHub account.
2. **Clone and Push to Your New Repository**: If cloning then take a local copy of this repo and then push it to your newly created repository:

```bash
git clone https://github.com/deploymenttheory/terraform-demo-jamfpro.git
cd terraform-demo-jamfpro
git remote set-url origin https://github.com/your-username/your-new-repo.git
git push -u origin main
```

Replace your-username and your-new-repo with your GitHub username and the name of your new repository.

3. **Configure Github Secrets**: Set up the following secrets in your GitHub repository settings:

- `TF_API_TOKEN`: Your Terraform Cloud API token for Terraform Cloud backend.
- `PAT_TOKEN`: Your GitHub Personal Access Token for branch management operations.

To set up the PAT_TOKEN:
a. Go to your GitHub Settings > Developer settings > Personal access tokens > Fine-grained tokens.
b. Click "Generate new token".
c. Give your token a descriptive name, e.g., "Terraform Jamf Pro Config Branch Management".
d. Set the expiration as per your security policies.
e. Under "Repository access", select "Only select repositories" and choose the repository you're setting up.
f. Under "Permissions", grant the following permissions:
- Repository permissions:
- Contents: Read and write (This allows branch management)
- Metadata: Read-only (This is required for API operations)
- Organization permissions:
- Members: Read-only (If working within an organization)
g. Click "Generate token" and copy the token immediately.
h. In your repository, go to Settings > Secrets and variables > Actions.
i. Click "New repository secret", name it PAT_TOKEN, and paste your token as the value.

Optional:

- `MSTEAMS_WEBHOOK_URL`: Your Microsoft Teams webhook URL for sending notifications.
- `SLACK_WEBHOOK_URL`: Your Slack webhook URL for sending notifications.

To set up the notification webhooks:

a. For Microsoft Teams:

- In your Teams channel, click the '...' next to the channel name and select 'Connectors'.
- Find 'Incoming Webhook' and click 'Configure'.
- Provide a name for your webhook and optionally upload an image.
- Click 'Create' and copy the webhook URL provided.
- In your GitHub repository, go to Settings > Secrets and variables > Actions.
- Click "New repository secret", name it MSTEAMS_WEBHOOK_URL, and paste the webhook URL as the value.

b. For Slack:

- Go to your Slack workspace's App Directory and create a new app (or use an existing one).
- Under 'Features', select 'Incoming Webhooks' and activate them.
- Click 'Add New Webhook to Workspace' and select the channel for notifications.
- Copy the webhook URL provided.
- In your GitHub repository, go to Settings > Secrets and variables > Actions.
- Click "New repository secret", name it SLACK_WEBHOOK_URL, and paste the webhook URL as the value.

These webhook URLs are used in the Send Notification workflow (send-notification.yml) to send deployment status updates to your team. The workflow determines which service to use based on the notification_channel input. Here's a snippet of how it's used:

4. **Configure Terraform Cloud Secrets**: Set up the following secrets in your Terraform Cloud workspace variable settings for each environment (Sandbox, Staging, Production):
    - `JAMFPRO_INSTANCE_FQDN`: Your Jamf Pro instance URL. For example: `https://your-instance.jamfcloud.com`.
    - `JAMFPRO_AUTH_METHOD`: Can be either `basic` or `oauth2`.
    - `JAMFPRO_CLIENT_ID`: Your Jamf Pro client id when `JAMFPRO_AUTH_METHOD` is set to 'oauth2'.
    - `JAMFPRO_CLIENT_SECRET`: Your Jamf Pro client secret when `JAMFPRO_AUTH_METHOD` is set to 'oauth2'.
    - `JAMFPRO_BASIC_AUTH_USERNAME`: Your Jamf Pro username when `JAMFPRO_AUTH_METHOD` is set to 'basic'.
    - `JAMFPRO_BASIC_AUTH_PASSWORD`: Your Jamf Pro user password when `JAMFPRO_AUTH_METHOD` is set to 'basic'.

   Note: For Terraform Cloud, when setting variables you do not need to prefix your env vars with `TF_VAR_` as Terraform Cloud automatically does this for you. Additionally, ensure to select the variable category as `Terraform variable`, with the HCL tickbox unchecked.

4. **Update Terraform Variables**: Modify the `terraform` block in your `.tf` files to match your Jamf Pro instance details. For example:

   ```hcl
   provider "jamfpro" {
     jamfpro_instance_fqdn                = var.jamfpro_instance_fqdn
     jamfpro_load_balancer_lock           = var.jamfpro_jamf_load_balancer_lock
     auth_method                          = var.jamfpro_auth_method
     client_id                            = var.jamfpro_client_id
     client_secret                        = var.jamfpro_client_secret
     log_level                            = var.jamfpro_log_level
     log_output_format                    = var.jamfpro_log_output_format
     log_console_separator                = var.jamfpro_log_console_separator
     log_export_path                      = var.jamfpro_log_export_path
     export_logs                          = var.jamfpro_export_logs
     hide_sensitive_data                  = var.jamfpro_hide_sensitive_data
     token_refresh_buffer_period_seconds  = var.jamfpro_token_refresh_buffer_period_seconds
     mandatory_request_delay_milliseconds = var.jamfpro_mandatory_request_delay_milliseconds
   }
   ```

   It's strongly recommended for beginners to ensure that `jamfpro_load_balancer_lock` is set to true, to avoid any issues with the Jamf Pro load balancer.

5. **Backend Configuration**: For our multi-environment setup, we'll be using Terraform workspaces. This approach allows us to use a single set of configuration files while maintaining separate states for each environment. Here's how to structure it:

   In your main Terraform configuration file (e.g., `main.tf`):

   ```hcl
    terraform {
      cloud {
        organization = "deploymenttheory"
        workspaces {
          tags = ["Jamf Pro"]
        }
      }
    }
   ```

   This configuration tells Terraform to use Terraform Cloud with the "deploymenttheory" organization and to work with any workspace tagged with "jamfpro".

   In Terraform Cloud:
   1. Create three workspaces:
      - `terraform-jamfpro-sandbox`
      - `terraform-jamfpro-staging`
      - `terraform-jamfpro-production`
   2. Tag each of these workspaces with the "jamfpro" tag.
   3. Set workspace-specific variables in Terraform Cloud for each environment. For example, you might have a variable `environment` set to "sandbox", "staging", or "production" in the respective workspaces.

   In your Terraform configuration, you can then use these workspace-specific variables to customize resources for each environment. For example:

   ```hcl
   resource "jamfpro_building" "example" {
     name = "Building-${var.environment}"
     // other attributes...
   }
   ```

   This approach ensures that each environment has its own isolated state in Terraform Cloud while allowing you to use a single set of configuration files. It provides flexibility in managing environment-specific configurations through Terraform Cloud workspace variables.

   Remember to set up appropriate access controls and variable values for each workspace in Terraform Cloud to maintain proper separation between environments.

6. **Terraform Provider Configuration**: Specify the provider source and version:

   ```hcl
   terraform {
     required_providers {
       jamfpro = {
         source  = "deploymenttheory/jamfpro"
         version = "0.1.12"
       }
     }
   }
   ```

7. **Define Your Resources**: Use Terraform resource definitions to manage your Jamf Pro resources.

8. **Create a New Branch**: When starting work on a new feature, bug fix, or any other change, create a new branch with an appropriate prefix. This naming convention is enforced by our workflows and helps categorize the type of work being done.

Use one of the following prefixes based on the nature of your work:

- `feat-`: For new features
- `fix-`: For bug fixes
- `docs-`: For documentation changes
- `style-`: For formatting, missing semi colons, etc; no code change
- `refactor-`: For refactoring production code
- `test-`: For adding missing tests, refactoring tests; no production code change
- `chore-`: For updating grunt tasks etc; no production code change
- `build-`: For changes that affect the build system or external dependencies
- `ci-`: For changes to our CI configuration files and scripts
- `perf-`: For performance improvements

To create a new branch:

1. Ensure you're on the main branch and it's up to date:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Create and switch to a new branch with an appropriate prefix:
   ```bash
   git checkout -b prefix-branch-name
   ```
   Replace `prefix-` with one of the prefixes listed above, and `branch-name` with a brief, descriptive name for your change.

   For example:
   ```bash
   git checkout -b feat-add-user-authentication
   ```

3. Make your changes on this new branch.

4. Push your branch to the remote repository:
   ```bash
   git push -u origin prefix-branch-name
   ```

This naming convention helps our automated workflows identify the type of change and process it accordingly. It also makes it easier for team members to understand the purpose of each branch at a glance.

9. **Make Changes and Push**: Make your changes and push to GitHub.

10. **Test in Sandbox**: The `01 - terraform testing: sandbox` workflow will automatically run.

11. **Promote to Sandbox**: After testing your changes in your feature branch, you can promote them to the Sandbox environment. This process involves creating a pull request to merge your feature branch into the `sandbox` branch. Here's how to do it:

- Ensure all your changes are committed and pushed to your feature branch.

- Go to your repository on GitHub.

- Click on the "Pull requests" tab.

- Click the "New pull request" button.

- Set the base branch to `sandbox` and the compare branch to your feature branch.

- Give your pull request a descriptive title and provide details about the changes in the description.

- Click "Create pull request".

- Request a review from your team members if required by your team's process.

- Once the pull request is approved, merge it into the `sandbox` branch.

Important: The actual application of changes to the Sandbox environment is handled automatically by the "02 - terraform apply to: sandbox" workflow. This workflow is triggered when a pull request is merged into the `sandbox` branch.

After merging:
- The workflow will automatically start.
- It will apply the Terraform changes to the Sandbox environment.
- You can monitor the progress of this workflow in the "Actions" tab of your GitHub repository.

Remember: Always verify that the workflow completes successfully. If there are any issues, they will be reported in the workflow run logs.

By following this process, you ensure that your changes are properly promoted to the Sandbox environment and applied in a controlled, automated manner.

12. **Promote to Staging**: Now manually trigger the `02-release-and-plan-staging.yml` workflow and approve the pull request to merge the release branch into the `staging` branch after change review.

13. **Apply to Staging**:

This project uses an automated process for creating versions and preparing releases when promoting changes from the Sandbox environment to Staging. This process is implemented in the `03 - release and terraform plan to: staging` workflow. Here's an overview of how it works:

### Triggering the Process

The release process is initiated manually. To start this process:

1. Go to the "Actions" tab in your GitHub repository.
2. Find the "03 - release and terraform plan to: staging" workflow.
3. Click "Run workflow".
4. Select the `sandbox` branch as the base for the release.
5. Click "Run workflow" to start the process.

### What Happens During the Process

Once triggered, the workflow performs the following steps:

1. **Version Creation**:
   - The workflow automatically determines the next version number based on semantic versioning principles.
   - It creates a new tag with this version number.
   - A new release is created in GitHub with this tag.

2. **Branch Creation**:
   - A new branch is created with the name pattern `release-v{version}-to-staging`.
   - This branch contains all the changes that were in the `sandbox` branch.

3. **Terraform Plan**:
   - The workflow runs a Terraform plan against the Staging environment.
   - This plan shows what changes will be applied to the Staging environment if this release is approved.

4. **Pull Request Creation**:
   - A pull request is automatically created to merge the release branch into the `staging` branch.
   - The pull request description includes:
     - The new version number
     - A summary of the Terraform plan (resources to be added, changed, or destroyed)
     - A link to the full Terraform plan in Terraform Cloud

### Next Steps

After the workflow completes:

1. Review the pull request and the Terraform plan carefully.
2. If everything looks correct, approve and merge the pull request.
3. Merging the pull request will trigger the "04 - terraform apply to: staging" workflow, which will apply the changes to the Staging environment.

### Important Notes

- Always review the Terraform plan before approving the release to Staging.
- The version number is automatically incremented. You don't need to manually manage version numbers.
- Each release creates a permanent tag in your repository's history, making it easy to track what changes were included in each release.
- If you need to make changes after creating a release but before applying to Staging, you can push additional commits to the release branch before merging the pull request.

This automated process ensures consistent versioning, provides a clear history of releases, and allows for a final review before applying changes to the Staging environment.

14. **Promote to Production**: Repeat the process for promoting to Production by manually triggering the `04-release-and-plan-production.yml` workflow and approving the pull request to merge the release branch into the `production` branch after change review.

15. **Apply to Production**: After the pull request is merged, the `05-terraform-apply-production.yml` workflow will automatically run to apply the changes to the Production environment.

## Example Terraform Resource

Below is an example of defining a building in Jamf Pro using Terraform:

```hcl
resource "jamfpro_building" "example_building" {
  name            = "Example Building"
  street_address1 = "123 Example St"
  street_address2 = "Suite 100"
  city            = "Example City"
  state_province  = "Example State"
  zip_postal_code = "12345"
  country         = "Example Country"
}
```