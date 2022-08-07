// Interface name
variable "interface_name" {
  type        = string
  description = "Name of our interface"
}

// Interface description
variable "interface_description" {
  type        = string
  description = "Name of our interface"
}

// Interface sub interface unit
variable "subinterface_unit" {
  type        = string
  description = "Sub interface unit number"
}

// Interface VLAN
variable "interface_vlan" {
  type        = string
  description = "VLAN assigned to interface"
}
