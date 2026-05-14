terraform {
  cloud {
    organization = "me-alejobarrios-dev"

    workspaces {
      name = "tdea-2026-01-cloud-computing"
    }
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}

  # --- NOTA IMPORTANTE PARA EJECUCIÓN LOCAL ---
  # El uso de 'use_msi = true' es exclusivo para ejecuciones desde adentro de Azure 
  # (por ejemplo, desde una Máquina Virtual de Azure o Azure Cloud Shell).
  # Para ejecuciones locales, Terraform utilizará automáticamente las credenciales de la CLI ('az login').

  # use_msi = true
  # client_id = var.managed_identity_client_id

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
