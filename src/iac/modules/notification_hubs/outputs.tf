output "hub_name" {
  value = azurerm_notification_hub.hub.name
}

output "primary_connection_string" {
  value     = azurerm_notification_hub_authorization_rule.hub_auth.primary_connection_string
  sensitive = true
}
