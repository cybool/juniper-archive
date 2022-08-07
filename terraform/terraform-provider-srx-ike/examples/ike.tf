terraform {
  cloud {
    organization = "cdot65"

    workspaces {
      name = "srx-ike"
    }
  }
  required_providers {
    srx-ike = {
      source  = "cdot65/srx-ike"
      version = "0.2.2"
    }
  }
}

provider "srx-ike" {
  host     = var.juniper_host_name
  port     = var.juniper_ssh_port
  sshkey   = var.juniper_ssh_key
  username = var.juniper_user_name
  password = var.juniper_user_password
}

module "enterprise-fw1" {
  source     = "./enterprise-fw1"
  providers  = { srx-ike = srx-ike }
  depends_on = [junos-ike_destroycommit.commit-main]
}

resource "junos-ike_commit" "commit-main" {
  resource_name = "commit"
  depends_on    = [module.enterprise-fw1]
}

resource "junos-ike_destroycommit" "commit-main" {
  resource_name = "destroycommit"
}