variable "subscription_id" {
  type        = string
  description = "ID de la suscripción de Azure"
  default     = "12bf58d3-730f-48a0-8dda-00944a58b1fa"
}

variable "tenant_id" {
  type        = string
  description = "ID del Tenant de Azure"
  default     = "ca3f1d6b-fd1f-40b1-b41a-488b980e9f7f"
}

variable "resource_group_name" {
  type        = string
  description = "Nombre del grupo de recursos existente"
  default     = "serverless_backend_application_mobile"
}

variable "managed_identity_client_id" {
  type        = string
  description = "Client ID de la User-Assigned Managed Identity"
  default     = "42cc9824-4b09-4a38-8ff2-4ddfc31ba84c"
}

variable "location" {
  type        = string
  description = "Ubicación de los recursos en Azure"
  default     = "eastus"
}

variable "fcm_api_key" {
  type        = string
  description = "Firebase Cloud Messaging API Key"
  sensitive   = true
}

variable "apns_certificate" {
  type        = string
  description = "Apple Push Notification Service Certificate"
  sensitive   = true
}

variable "jwt_secret" {
  type        = string
  description = "Secreto compartido utilizado para firmar y validar los tokens JWT"
  sensitive   = true
}
