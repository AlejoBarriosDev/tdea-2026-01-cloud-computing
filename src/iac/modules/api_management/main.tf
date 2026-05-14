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
}

resource "azurerm_api_management_api_policy" "rapidgo_policy" {
  api_name            = azurerm_api_management_api.rapidgo_api.name
  api_management_name = azurerm_api_management_api.rapidgo_api.api_management_name
  resource_group_name = var.resource_group_name

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
