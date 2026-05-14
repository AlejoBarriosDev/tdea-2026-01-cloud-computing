output "primary_sql_connection_string" {
  value     = azurerm_cosmosdb_account.cosmos.primary_sql_connection_string
  sensitive = true
}
