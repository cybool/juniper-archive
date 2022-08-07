terraform {
  required_providers {
    junos-ex-mstp = {
      source  = "cdot65/junos-ex-mstp"
      version = "0.0.2"
    }
  }
}

// MSTP Bridge Priority
resource "junos-ex-mstp_ProtocolsMstpBridge__Priority" "bridge_priority" {
  resource_name    = "mstp_bridge_priority"
  bridge__priority = "32k"
}

// MSTP Configuration Name
resource "junos-ex-mstp_ProtocolsMstpConfiguration__Name" "configuration_name" {
  resource_name       = "mstp_config_name"
  configuration__name = "brookefield"
}

// MSTP Interface Edge
resource "junos-ex-mstp_ProtocolsMstpInterfaceEdge" "edge_interface" {
  resource_name = "mstp_edge_interface"
  edge          = ""
  name          = "all"
}

// MSTP Interface Mode
resource "junos-ex-mstp_ProtocolsMstpInterfaceMode" "uplink_interface" {
  resource_name = "mstp_uplink_interface"
  mode          = "point-to-point"
  name          = "ge-0/0/11"
}

// MSTP MST VLANs
resource "junos-ex-mstp_ProtocolsMstpMstiVlan" "msti_vlans" {
  resource_name = "msti_vlans_group"
  name          = "1"
  vlan          = "1-4094"
}
