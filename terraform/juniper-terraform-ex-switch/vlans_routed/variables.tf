// VLAN name
variable "vlan_name" {
  type        = string
  description = "Name of our VLAN"
}

// VLAN description
variable "vlan_description" {
  type        = string
  description = "Description of our vlan"
}

// Name of our VLAN description configuration group
variable "vlan_description_group" {
  type        = string
  description = "Name used for the VLAN description configuration group"
}

// VLAN ID
variable "vlan_id" {
  type        = string
  description = "VLAN ID"
}

// Name of our VLAN ID configuration group
variable "vlan_id_group" {
  type        = string
  description = "Name used for the VLAN ID configuration group"
}

// Layer 3 Interface
variable "vlan_l3iface" {
  type        = string
  description = "Routed interface for the VLAN"
}

// Name of our L3 interface configuration group
variable "vlan_l3iface_group" {
  type        = string
  description = "Name used for the L3 interface configuration group"
}

