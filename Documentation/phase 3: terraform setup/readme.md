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

This should make the files needed to start your terraform configuration.

Here is mine when I was done
```bash
# Configure the AzureRM Provider
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>3.0" # Use a compatible version, ~>3.0 means 3.x.x
    }
    random = {
      source = "hashicorp/random"
      version = "~>3.0"
    }
  }
  required_version = ">= 1.0.0" # Ensure your Terraform CLI is compatible
}

# Provider block for Azure
provider "azurerm" {
  features {} # This block is required for the AzureRM provider
}

# Data source to get current client configuration (needed for tenant_id)
data "azurerm_client_config" "current" {}

# Resource Group
resource "azurerm_resource_group" "cloud_cafe_rg_tf" {
    name     = "Cloud-Cafe-Orders-TF-RG"
    location = var.azure_region
}

# Azure SQL Server
resource "azurerm_mssql_server" "cloud_cafe_sql_server_tf" {
  name                         = "cloudcafetf-${random_string.suffix.result}"
  resource_group_name          = azurerm_resource_group.cloud_cafe_rg_tf.name
  location                     = azurerm_resource_group.cloud_cafe_rg_tf.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password

  tags = {
    environment = "terraform-managed"
    project     = "CloudCafe"
  }
}

# Azure SQL Database
resource "azurerm_mssql_database" "cloud_cafe_orders_db_tf" {
  name                = "cloud-cafe-ordersDB-tf"
  server_id           = azurerm_mssql_server.cloud_cafe_sql_server_tf.id
  collation           = "SQL_Latin1_General_CP1_CI_AS"
  sku_name            = "Basic"

  tags = {
    environment = "terraform-managed"
    project     = "CloudCafe"
  }
}

# SQL Server Firewall Rule to allow Azure services
resource "azurerm_sql_firewall_rule" "allow_azure_services_sql_tf" {
  name                = "AllowAzureServices"
  server_name         = azurerm_mssql_server.cloud_cafe_sql_server_tf.name
  resource_group_name = azurerm_resource_group.cloud_cafe_rg_tf.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

# SQL Server Active Directory Administrator
resource "azurerm_sql_active_directory_administrator" "aad_admin_tf" {
  server_name         = azurerm_mssql_server.cloud_cafe_sql_server_tf.name
  resource_group_name = azurerm_resource_group.cloud_cafe_rg_tf.name
  login_name          = var.aad_admin_username
  object_id           = var.aad_admin_object_id
  tenant_id           = data.azurerm_client_config.current.tenant_id
}

# Azure Storage Account
resource "azurerm_storage_account" "cloud_cafe_sa_tf" {
  name                     = "cloudcftfsa${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.cloud_cafe_rg_tf.name
  location                 = azurerm_resource_group.cloud_cafe_rg_tf.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "terraform-managed"
    project     = "CloudCafe"
  }
}

# Azure Storage Queue
resource "azurerm_storage_queue" "orders_queue_tf" {
  name                  = "ordersqueuetf"
  storage_account_name  = azurerm_storage_account.cloud_cafe_sa_tf.name
}

# Helper for unique naming
resource "random_string" "suffix" {
  length  = 5
  special = false
  upper   = false
  numeric = true
}
```
****UPDATE WITH FINISHED IaC WHEN DONE****

After that make sure you have the proper networking so that you don't get blocked when performing queries.

<img width="1570" height="657" alt="image" src="https://github.com/user-attachments/assets/22c3652d-9db2-4572-bd92-7e7508a722f9" />

Add your client

Next you'll have to add your tables again

perfrom this query to make all the tables

```bash
CREATE TABLE Orders (
    OrderId NVARCHAR(50) PRIMARY KEY,
    ItemName NVARCHAR(100) NOT NULL,
    Quantity INT NOT NULL,
    CustomerName NVARCHAR(100),
    OrderDate DATETIME NOT NULL DEFAULT GETDATE(),
    Status NVARCHAR(50) NOT NULL,
    ProcessedByFunctionId NVARCHAR(100) NULL
);
```

Next make sure that you have proper access
```bash
CREATE USER [cloudcafeproc-tf-3v1ky] FROM EXTERNAL PROVIDER;
GRANT INSERT ON Orders TO [cloudcafeproc-tf-3v1ky];
GRANT SELECT ON Orders TO [cloudcafeproc-tf-3v1ky];
```


