output "default_hostname" {
  value = azurerm_linux_function_app.func_app.default_hostname
}

output "app_insights_instrumentation_key" {
  value = azurerm_application_insights.app_insights.instrumentation_key
}

output "app_insights_id" {
  value = azurerm_application_insights.app_insights.id
}
