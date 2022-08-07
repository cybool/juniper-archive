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
  resource_name = var.vlan_description_group
  name          = var.vlan_name
  description   = var.vlan_description
}

// Routed Interface
resource "junos-ex-vlans_VlansVlanL3__Interface" "vlan_l3iface" {
  resource_name = var.vlan_l3iface_group
  l3__interface = var.vlan_l3iface
  name          = var.vlan_name
}

// VLAN ID
resource "junos-ex-vlans_VlansVlanVlan__Id" "vlans" {
  resource_name = var.vlan_id_group
  vlan__id      = var.vlan_id
  name          = var.vlan_name
}
