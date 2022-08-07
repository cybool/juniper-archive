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

// Interface VLANs
variable "interface_vlans" {
  type        = string
  description = "VLANs assigned to interface"
}

// Interface mode
variable "interface_mode" {
  type        = string
  description = "Access or Trunk mode"
}

// Apply Group Names
variable "interface_description_group" {
  type        = string
  description = "Name of interface description apply group"
}

variable "interface_mode_group" {
  type        = string
  description = "Name of interface mode apply group"
}

variable "interface_vlans_group" {
  type        = string
  description = "Name of interface VLAN members apply group"
}
