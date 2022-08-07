terraform {
  required_providers {
    junos-interfaces = {
      source  = "cdot65/junos-interfaces"
      version = "0.0.1"
    }
  }
}

provider "junos-interfaces" {
  host     = "192.168.105.10"
  port     = var.juniper_ssh_port
  sshkey   = var.juniper_ssh_key
  username = var.juniper_user_name
  password = var.juniper_user_password
}

module "interfaces" {
  // interface lo0 description "WAN interface provisioned with Terraform"
  // interface lo0 unit 0 family inet 74.51.0.2/24"
  apply_group_name      = "cdot65_interfaces"
  interface_name        = "ge-0/0/0"
  interface_description = "WAN interface"
  subinterface_unit     = "0"
  subinterface_address  = "74.51.0.2/24"

  // passing information into our provider
  source     = "./interfaces"
  providers  = { junos-interfaces = junos-interfaces }
  depends_on = [junos-interfaces_destroycommit.commit-main]
}

resource "junos-interfaces_commit" "commit-main" {
  resource_name = "commit"
  depends_on    = [module.interfaces]
}

resource "junos-interfaces_destroycommit" "commit-main" {
  resource_name = "destroycommit"
}
