variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Location for resources"
  type        = string
}

variable "storage_account_name" {
  description = "Name of the storage account for functions"
  type        = string
}

variable "storage_account_access_key" {
  description = "Access key of the storage account for functions"
  type        = string
  sensitive   = true
}

variable "cosmos_db_connection_string" {
  description = "Connection string for Cosmos DB"
  type        = string
  sensitive   = true
}

variable "blob_storage_connection_string" {
  description = "Connection string for Blob Storage"
  type        = string
  sensitive   = true
}

variable "notification_hub_connection_string" {
  description = "Connection string for Notification Hub"
  type        = string
  sensitive   = true
}

variable "notification_hub_name" {
  description = "Name of the Notification Hub"
  type        = string
}

variable "fcm_api_key" {
  description = "Firebase Cloud Messaging API Key"
  type        = string
  sensitive   = true
}

variable "apns_certificate" {
  description = "Apple Push Notification Service Certificate"
  type        = string
  sensitive   = true
}
