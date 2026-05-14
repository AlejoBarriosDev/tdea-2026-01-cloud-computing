# Referencia al grupo de recursos existente
data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

# Generamos un sufijo aleatorio para evitar problemas con nombres únicos globales (como Storage Accounts)
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

# Componente básico de prueba: Una cuenta de almacenamiento (Storage Account)
resource "azurerm_storage_account" "test_sa" {
  name                     = "starapidgotest${random_string.suffix.result}"
  resource_group_name      = data.azurerm_resource_group.rg.name
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "dev"
    project     = "rapidgo"
  }
}
