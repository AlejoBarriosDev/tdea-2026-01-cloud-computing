resource "azurerm_storage_account" "storage_backend" {
  name                     = "strapidgobackenddata"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}

resource "azurerm_storage_container" "comprobantes" {
  name                  = "comprobantes"
  storage_account_name  = azurerm_storage_account.storage_backend.name
  container_access_type = "private"
}
