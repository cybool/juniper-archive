terraform {
  required_providers {
    junos-ex-vlans = {
      source  = "cdot65/junos-ex-vlans"
      version = "0.0.1"
    }
  }
}

// VLAN Description
resource "junos-ex-vlans_VlansVlanDescription" "vlan_description" {
  resource_name = "vlan_103_description"
  name          = var.vlan_name
  description   = var.vlan_description
}

// Interface Mode
// resource "junos-ex-vlans_VlansVlanL3__Interface" "vlan_l3iface" {
//   resource_name = "vlan_103_L3_iface"
//   l3__interface = "irb.103"
//   name          = var.vlan_name
// }

// VLAN ID
resource "junos-ex-vlans_VlansVlanVlan__Id" "vlans" {
  resource_name = "vlan_103_id"
  vlan__id      = var.vlan_id
  name          = var.vlan_name
}
