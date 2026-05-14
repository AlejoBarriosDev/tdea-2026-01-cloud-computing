resource "azurerm_notification_hub_namespace" "nh_namespace" {
  name                = "ns-rapidgo-notifications"
  resource_group_name = var.resource_group_name
  location            = var.location
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
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource "azurerm_notification_hub_authorization_rule" "hub_auth" {
  name                  = "rapidgo-auth"
  namespace_name        = azurerm_notification_hub_namespace.nh_namespace.name
  notification_hub_name = azurerm_notification_hub.hub.name
  resource_group_name   = var.resource_group_name
  manage                = true
  send                  = true
  listen                = true
}
