resource "azurerm_api_management" "apim" {
  name                = "apim-rapidgo-gateway"
  location            = var.location
  resource_group_name = var.resource_group_name
  publisher_name      = "RapidGo Corp"
  publisher_email     = "admin@rapidgo.com"
  sku_name            = "Developer_1"

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}

resource "azurerm_api_management_api" "rapidgo_api" {
  name                = "rapidgo-api"
  resource_group_name = var.resource_group_name
  api_management_name = azurerm_api_management.apim.name
  revision            = "1"
  display_name        = "RapidGo API"
  path                = "api"
  protocols           = ["https"]
  service_url         = "https://${var.function_default_hostname}/api"
  subscription_required = true
}

resource "azurerm_api_management_product" "rapidgo_product" {
  product_id            = "rapidgo-services"
  api_management_name   = azurerm_api_management.apim.name
  resource_group_name   = var.resource_group_name
  display_name          = "RapidGo Services"
  subscription_required = true
  approval_required     = false
  published             = true
}

resource "azurerm_api_management_product_api" "rapidgo_product_api" {
  api_name            = azurerm_api_management_api.rapidgo_api.name
  product_id          = azurerm_api_management_product.rapidgo_product.product_id
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
}

resource "azurerm_api_management_subscription" "rapidgo_sub" {
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
  product_id          = azurerm_api_management_product.rapidgo_product.id
  display_name        = "RapidGo App Subscription"
  state               = "active"
}

resource "azurerm_api_management_named_value" "jwt_secret" {
  name                = "jwt-secret-key"
  resource_group_name = var.resource_group_name
  api_management_name = azurerm_api_management.apim.name
  display_name        = "jwt-secret-key"
  value               = var.jwt_secret
  secret              = true
}

resource "azurerm_api_management_api_policy" "rapidgo_policy" {
  api_name            = azurerm_api_management_api.rapidgo_api.name
  api_management_name = azurerm_api_management_api.rapidgo_api.api_management_name
  resource_group_name = var.resource_group_name

  xml_content = <<XML
<policies>
  <inbound>
    <base />
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401" require-scheme="Bearer">
      <issuer-signing-keys>
        <key>{{${azurerm_api_management_named_value.jwt_secret.name}}}</key>
      </issuer-signing-keys>
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

resource "azurerm_api_management_logger" "apim_logger" {
  name                = "rapidgo-logger"
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
  resource_id         = var.app_insights_id

  application_insights {
    instrumentation_key = var.app_insights_instrumentation_key
  }
}

resource "azurerm_api_management_api_diagnostic" "rapidgo_diag" {
  identifier               = "applicationinsights"
  resource_group_name      = var.resource_group_name
  api_management_name      = azurerm_api_management.apim.name
  api_name                 = azurerm_api_management_api.rapidgo_api.name
  api_management_logger_id = azurerm_api_management_logger.apim_logger.id

  sampling_percentage       = 100.0
  always_log_errors         = true
  log_client_ip             = true
  verbosity                 = "verbose"
  http_correlation_protocol = "W3C"

  frontend_request {
    body_bytes = 32
    headers_to_log = [
      "content-type",
      "accept",
      "origin",
    ]
  }

  frontend_response {
    body_bytes = 32
    headers_to_log = [
      "content-type",
      "content-length",
    ]
  }

  backend_request {
    body_bytes = 32
    headers_to_log = [
      "content-type",
      "accept",
      "origin",
    ]
  }

  backend_response {
    body_bytes = 32
    headers_to_log = [
      "content-type",
      "content-length",
    ]
  }
}

resource "azurerm_api_management_api_operation" "registrar_pedido" {
  operation_id        = "registrarPedido"
  api_name            = azurerm_api_management_api.rapidgo_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
  display_name        = "Registrar Pedido"
  method              = "POST"
  url_template        = "/pedidos"
  description         = "Registra un nuevo pedido en el sistema"
}

resource "azurerm_api_management_api_operation" "consultar_historial" {
  operation_id        = "consultarHistorial"
  api_name            = azurerm_api_management_api.rapidgo_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
  display_name        = "Consultar Historial"
  method              = "GET"
  url_template        = "/pedidos"
  description         = "Consulta el historial de pedidos"
}

resource "azurerm_api_management_api_operation" "actualizar_estado" {
  operation_id        = "actualizarEstado"
  api_name            = azurerm_api_management_api.rapidgo_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
  display_name        = "Actualizar Estado"
  method              = "PUT"
  url_template        = "/pedidos/{id}"
  description         = "Actualiza el estado de un pedido"

  template_parameter {
    name     = "id"
    type     = "string"
    required = true
  }
}
