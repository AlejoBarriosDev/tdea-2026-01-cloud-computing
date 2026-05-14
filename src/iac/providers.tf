terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0" # Puedes ajustar la versión según sea necesario
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}

  # --- NOTA IMPORTANTE PARA EJECUCIÓN LOCAL ---
  # El uso de 'use_msi = true' solo funciona si ejecutas Terraform DESDE adentro de Azure 
  # (por ejemplo, desde una Máquina Virtual de Azure o Azure Cloud Shell).
  # Como estás ejecutando esto desde tu computador local, Terraform buscará la IP interna de Azure y fallará.
  # Para ejecutarlo localmente, Terraform usará automáticamente tu sesión de 'az login'.

  # use_msi = true
  # client_id = var.managed_identity_client_id

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
