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
