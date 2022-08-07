terraform {
  required_providers {
    junos-ex-interfaces = {
      source  = "cdot65/junos-ex-interfaces"
      version = "0.0.2"
    }
  }
}

// Interface Description
resource "junos-ex-interfaces_InterfacesInterfaceDescription" "interface_description" {
  resource_name = "iface_ge-0/0/0_description"
  name          = var.interface_name
  description   = var.interface_description
}

// Interface Mode
resource "junos-ex-interfaces_InterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__Mode" "subinterface_address" {
  resource_name   = "iface_ge-0/0/0_mode"
  interface__mode = "access"
  name            = var.interface_name
  name__1         = var.subinterface_unit
}

// VLANs
resource "junos-ex-interfaces_InterfacesInterfaceUnitFamilyEthernet__SwitchingVlanMembers" "vlans" {
  resource_name = "iface_ge-0/0/0_vlans"
  members       = var.interface_vlan
  name          = var.interface_name
  name__1       = var.subinterface_unit
}
