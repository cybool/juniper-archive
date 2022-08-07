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
  resource_name = var.interface_description_group
  name          = var.interface_name
  description   = var.interface_description
}

// Interface Mode
resource "junos-ex-interfaces_InterfacesInterfaceUnitFamilyEthernet__SwitchingInterface__Mode" "interface_mode" {
  resource_name   = var.interface_mode_group
  interface__mode = var.interface_mode
  name            = var.interface_name
  name__1         = var.subinterface_unit
}

// VLANs
resource "junos-ex-interfaces_InterfacesInterfaceUnitFamilyEthernet__SwitchingVlanMembers" "interface_vlans" {
  resource_name = var.interface_vlans_group
  members       = var.interface_vlans
  name          = var.interface_name
  name__1       = var.subinterface_unit
}
