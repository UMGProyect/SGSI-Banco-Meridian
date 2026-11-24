variable "project_id" {
  type        = string
  description = "ID del proyecto independiente. Nunca el ID de TCP/IP."
  validation {
    condition     = can(regex("^sgsi-banco-meridian[a-z0-9-]*$", var.project_id))
    error_message = "Use un ID nuevo con prefijo sgsi-banco-meridian."
  }
}
variable "region" {
  type    = string
  default = "us-central1"
}
variable "zone" {
  type    = string
  default = "us-central1-a"
}
variable "enable_vms" {
  type        = bool
  default     = false
  description = "Activa tres VMs privadas; genera cargos."
}
variable "enable_nat" {
  type        = bool
  default     = false
  description = "Activa NAT de salida; genera cargos."
}
