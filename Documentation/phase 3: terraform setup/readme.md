Now that we have setup many different Azure resources lets set up a terraform to set this up quickly and break it down quickly

First install terraform and put it in your path

Make a new folder for terraform configurations

Once in put in this code to configure your setup. Make a main.tf

```bash
# Configure the AzureRM Provider
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>3.0" # Use a compatible version, ~>3.0 means 3.x.x
    }
  }
  required_version = ">= 1.0.0" # Ensure your Terraform CLI is compatible
}

# Provider block for Azure
provider "azurerm" {
  features {} # This block is required for the AzureRM provider
}
```
Save the file then open a terminal and put in

```bash
terraform init
```
