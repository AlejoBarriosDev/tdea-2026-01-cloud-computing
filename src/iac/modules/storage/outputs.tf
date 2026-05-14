output "storage_account_name" {
  value = azurerm_storage_account.storage_backend.name
}

output "primary_access_key" {
  value     = azurerm_storage_account.storage_backend.primary_access_key
  sensitive = true
}

output "primary_connection_string" {
  value     = azurerm_storage_account.storage_backend.primary_connection_string
  sensitive = true
}
