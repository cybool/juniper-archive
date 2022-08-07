terraform {
  required_providers {
    junos-ex-interfaces = {
      source  = "cdot65/junos-ex-interfaces"
      version = "0.0.2"
    }
  }
}

provider "junos-ex-interfaces" {
  host     = "office"
  port     = var.juniper_ssh_port
  sshkey   = var.juniper_ssh_key
  username = var.juniper_user_name
  password = var.juniper_user_password
}

module "interfaces" {
  // interface lo0 description "provisioned with Terraform"
  // interface lo0 unit 0 family inet 10.1.2.3/32"
  interface_name        = "ge-0/0/0"
  interface_description = "tf: Raspberry Pi"
  subinterface_unit     = "0"
  interface_vlan        = "VLAN_104"

  // passing information into our provider
  source     = "./interfaces"
  providers  = { junos-ex-interfaces = junos-ex-interfaces }
  depends_on = [junos-ex-interfaces_destroycommit.commit-main]
}

resource "junos-ex-interfaces_commit" "commit-main" {
  resource_name = "commit"
  depends_on    = [module.interfaces]
}

resource "junos-ex-interfaces_destroycommit" "commit-main" {
  resource_name = "destroycommit"
}
