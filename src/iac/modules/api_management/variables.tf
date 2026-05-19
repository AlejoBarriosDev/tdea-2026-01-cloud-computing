variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Location for resources"
  type        = string
}

variable "function_default_hostname" {
  description = "The default hostname of the Azure Function App"
  type        = string
}

variable "jwt_secret" {
  description = "JWT Secret for API Management validation"
  type        = string
  sensitive   = true
}

variable "app_insights_instrumentation_key" {
  description = "Application Insights Instrumentation Key"
  type        = string
}

variable "app_insights_id" {
  description = "Application Insights Resource ID"
  type        = string
}
