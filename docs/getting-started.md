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

8. **Create a New Branch**: Create a new branch with the appropriate prefix eg. (`feature-`, `bugfix-`, or `chore-`).

9. **Make Changes and Push**: Make your changes and push to GitHub.

10. **Test in Sandbox**: The `01 - terraform testing: sandbox` workflow will automatically run.

11. **Promote to Sandbox**: After testing in Sandbox, create a pull request to merge all chanages from your short lived branch into the `sandbox` branch.

12. **Promote to Staging**: Now manually trigger the `02-release-and-plan-staging.yml` workflow and approve the pull request to merge the release branch into the `staging` branch after change review.

13. **Apply to Staging**: After the pull request is merged, the `03-terraform-apply-staging.yml` workflow will automatically run to apply the changes to the Staging environment.

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