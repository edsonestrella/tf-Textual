# Basic Usage Examples

## Azure Terraform Project

1. Navigate to your Azure Terraform project:

````bash
cd ~/projects/azure-infra
````

2. Launch tf-textual:

````bash
tf-textual
````

3. The app will auto-detect:
   - Azure provider configuration
   - Subscription context from Azure CLI
   - `.tfvars` files in the directory
   - Current state backend

4. Use the workflow:
   - Press `Ctrl+I` or click `🚀 Init` to initialize
   - Press `Ctrl+P` or click `📋 Plan` to see changes
   - Press `Ctrl+A` or click `✅ Apply` to deploy

## Multi-environment Setup

For projects with multiple environments:

````bash
# Development
cd infrastructure/dev
tf-textual

# Production  
cd infrastructure/prod
tf-textual --var-file production.tfvars
````

## AWS Example

For AWS projects, ensure you have AWS credentials configured:

````bash
# With specific AWS profile
AWS_PROFILE=production tf-textual

# Or with environment variables
AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=xxx tf-textual
````

## Google Cloud Example

For GCP projects, ensure authentication:

````bash
# Authenticate with gcloud
gcloud auth application-default login

# Launch tf-textual
tf-textual
````

## Keyboard-Driven Workflow

1. `Ctrl+I` - Initialize Terraform
2. `Ctrl+P` - Plan and review changes
3. `Ctrl+A` - Apply approved plan
4. `Ctrl+R` - Refresh state view
5. `F1` - Toggle dark/light mode

## Common Scenarios

### First-time Setup
````bash
cd new-terraform-project
tf-textual
# Click 🚀 Init or press Ctrl+I
# Click 📋 Plan or press Ctrl+P to see initial plan
# Click ✅ Apply or press Ctrl+A to create resources
````

### Making Changes
````bash
# Edit your .tf files
vim main.tf
# Then in tf-textual:
# Click 📋 Plan to see changes
# Click ✅ Apply to deploy changes
````

### Working with Modules
````bash
# tf-textual automatically detects and displays:
# - Root module resources
# - Child module resources
# - Module dependencies
````

## Troubleshooting

### Authentication Issues
- Azure: Run `az login`
- AWS: Configure AWS credentials
- GCP: Run `gcloud auth application-default login`

### Terraform Not Found
Ensure Terraform is installed and in your PATH:

````bash
terraform version
````

### State File Issues
If state is corrupted or locked:

````bash
# tf-textual will show appropriate error messages
# Use standard Terraform commands to resolve:
terraform force-unlock [LOCK_ID]
terraform refresh
````

Enjoy visualizing your infrastructure! 🌟
