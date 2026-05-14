# Referencia al grupo de recursos existente
data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

module "storage" {
  source              = "./modules/storage"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
}

module "cosmosdb" {
  source              = "./modules/cosmosdb"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
}

module "notification_hubs" {
  source              = "./modules/notification_hubs"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
}

module "functions" {
  source                             = "./modules/functions"
  resource_group_name                = data.azurerm_resource_group.rg.name
  location                           = data.azurerm_resource_group.rg.location
  storage_account_name               = module.storage.storage_account_name
  storage_account_access_key         = module.storage.primary_access_key
  cosmos_db_connection_string        = module.cosmosdb.primary_sql_connection_string
  blob_storage_connection_string     = module.storage.primary_connection_string
  notification_hub_connection_string = module.notification_hubs.primary_connection_string
  notification_hub_name              = module.notification_hubs.hub_name
  fcm_api_key                        = var.fcm_api_key
  apns_certificate                   = var.apns_certificate
}

module "api_management" {
  source                    = "./modules/api_management"
  resource_group_name       = data.azurerm_resource_group.rg.name
  location                  = data.azurerm_resource_group.rg.location
  function_default_hostname = module.functions.default_hostname
}
