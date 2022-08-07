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
