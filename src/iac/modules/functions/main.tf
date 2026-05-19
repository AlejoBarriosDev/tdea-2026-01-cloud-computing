resource "azurerm_log_analytics_workspace" "law" {
  name                = "law-rapidgo"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "app_insights" {
  name                = "ai-rapidgo"
  resource_group_name = var.resource_group_name
  location            = var.location
  workspace_id        = azurerm_log_analytics_workspace.law.id
  application_type    = "web"
}

resource "azurerm_service_plan" "func_plan" {
  name                = "ASP-serverlessbackendapplicationmob-81a0"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "FC1" 
}

resource "azurerm_linux_function_app" "func_app" {
  name                       = "func-rapidgo-backend"
  resource_group_name        = var.resource_group_name
  location                   = var.location
  service_plan_id            = azurerm_service_plan.func_plan.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key

  site_config {
    application_insights_key               = azurerm_application_insights.app_insights.instrumentation_key
    application_insights_connection_string = azurerm_application_insights.app_insights.connection_string
    
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"           = "python"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"     = "true"
    "COSMOS_DB_CONNECTION_STRING"        = var.cosmos_db_connection_string
    "BLOB_STORAGE_CONNECTION_STRING"     = var.blob_storage_connection_string
    "NOTIFICATION_HUB_CONNECTION_STRING" = var.notification_hub_connection_string
    "NOTIFICATION_HUB_NAME"              = var.notification_hub_name
    "FCM_API_KEY"                        = var.fcm_api_key
    "APNS_CERTIFICATE"                   = var.apns_certificate
    "DEPLOYMENT_STORAGE_CONNECTION_STRING" = var.blob_storage_connection_string
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.app_insights.connection_string
  }

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}
