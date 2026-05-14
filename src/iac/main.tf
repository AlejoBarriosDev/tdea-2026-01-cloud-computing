# Referencia al grupo de recursos existente
data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

# 1. API Management (Gateway)
resource "azurerm_api_management" "apim" {
  name                = "apim-rapidgo-gateway"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  publisher_name      = "RapidGo Corp"
  publisher_email     = "admin@rapidgo.com"
  sku_name            = "Developer_1"

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}

# 1.1 API Management API
resource "azurerm_api_management_api" "rapidgo_api" {
  name                = "rapidgo-api"
  resource_group_name = data.azurerm_resource_group.rg.name
  api_management_name = azurerm_api_management.apim.name
  revision            = "1"
  display_name        = "RapidGo API"
  path                = "api"
  protocols           = ["https"]
}

# 1.2 API Management Policy (Throttling & JWT)
resource "azurerm_api_management_api_policy" "rapidgo_policy" {
  api_name            = azurerm_api_management_api.rapidgo_api.name
  api_management_name = azurerm_api_management_api.rapidgo_api.api_management_name
  resource_group_name = data.azurerm_resource_group.rg.name

  xml_content = <<XML
<policies>
  <inbound>
    <base />
    <rate-limit calls="100" renewal-period="60" />
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401" failed-validation-error-message="Unauthorized">
      <openid-config url="https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration" />
    </validate-jwt>
  </inbound>
  <backend>
    <base />
  </backend>
  <outbound>
    <base />
  </outbound>
  <on-error>
    <base />
  </on-error>
</policies>
XML
}

# 2. Storage Account para las Functions y Blob Storage
resource "azurerm_storage_account" "storage_backend" {
  name                     = "strapidgobackenddata"
  resource_group_name      = data.azurerm_resource_group.rg.name
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}

# 2.1 Blob Storage Container para comprobantes
resource "azurerm_storage_container" "comprobantes" {
  name                  = "comprobantes"
  storage_account_name  = azurerm_storage_account.storage_backend.name
  container_access_type = "private"
}

# 3. Cosmos DB (NoSQL)
resource "azurerm_cosmosdb_account" "cosmos" {
  name                = "cosmos-rapidgo-nosql"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  free_tier_enabled = true

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = data.azurerm_resource_group.rg.location
    failover_priority = 0
    zone_redundant    = false
  }

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}

# 3.1 Cosmos DB Database
resource "azurerm_cosmosdb_sql_database" "db" {
  name                = "rapidgo-db"
  resource_group_name = data.azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmos.name
}

# 3.2 Cosmos DB Container
resource "azurerm_cosmosdb_sql_container" "pedidos" {
  name                  = "pedidos"
  resource_group_name   = data.azurerm_resource_group.rg.name
  account_name          = azurerm_cosmosdb_account.cosmos.name
  database_name         = azurerm_cosmosdb_sql_database.db.name
  partition_key_paths   = ["/id"]
  partition_key_version = 1
}

# 4. Azure Functions (Serverless Backend)
resource "azurerm_service_plan" "func_plan" {
  name                = "plan-rapidgo-functions"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1" # Consumption Plan
}

resource "azurerm_linux_function_app" "func_app" {
  name                       = "func-rapidgo-backend"
  resource_group_name        = data.azurerm_resource_group.rg.name
  location                   = data.azurerm_resource_group.rg.location
  service_plan_id            = azurerm_service_plan.func_plan.id
  storage_account_name       = azurerm_storage_account.storage_backend.name
  storage_account_access_key = azurerm_storage_account.storage_backend.primary_access_key

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "COSMOS_DB_CONNECTION_STRING"        = azurerm_cosmosdb_account.cosmos.primary_sql_connection_string
    "BLOB_STORAGE_CONNECTION_STRING"     = azurerm_storage_account.storage_backend.primary_connection_string
    "NOTIFICATION_HUB_CONNECTION_STRING" = azurerm_notification_hub_authorization_rule.hub_auth.primary_connection_string
    "NOTIFICATION_HUB_NAME"              = azurerm_notification_hub.hub.name
    "FCM_API_KEY"                        = var.fcm_api_key
    "APNS_CERTIFICATE"                   = var.apns_certificate
    "FUNCTIONS_WORKER_RUNTIME"           = "python"
  }

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}

# 5. Notification Hubs
resource "azurerm_notification_hub_namespace" "nh_namespace" {
  name                = "ns-rapidgo-notifications"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  namespace_type      = "NotificationHub"
  sku_name            = "Free"

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}

resource "azurerm_notification_hub" "hub" {
  name                = "hub-rapidgo-push"
  namespace_name      = azurerm_notification_hub_namespace.nh_namespace.name
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
}

# 5.1 Notification Hub Authorization Rule
resource "azurerm_notification_hub_authorization_rule" "hub_auth" {
  name                  = "rapidgo-auth"
  namespace_name        = azurerm_notification_hub_namespace.nh_namespace.name
  notification_hub_name = azurerm_notification_hub.hub.name
  resource_group_name   = data.azurerm_resource_group.rg.name
  manage                = true
  send                  = true
  listen                = true
}
