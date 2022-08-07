# Juniper Terraform Example: Configure EX switch

[![N|Solid](https://raw.githubusercontent.com/cdot65/juniper-terraform-srx/dev/site/content/assets/images/topology.png)](https://juniper.net/)

## Overview

The goal of this project is to provide an example method to interact with Juniper EX products with Terraform.

### VLANs

We will need to create several VLAN objects, some with routed interfaces and others without.

- create vlan with a name of VLAN_103
- apply a description of `tf: devops VLAN` to our new vlan
- associate a routed interface to this vlan (optional)

```
VLAN_103 {
    description "tf: devops VLAN";
    vlan-id 103;
}
```

### Interfaces

Interfaces are configured in layer 2 mode exclusively, as of now. Will update later to support routed interfaces.

- create interface
- apply a description to our new interface
- create a sub-interface with a unit ID
- set interface to ethernet-switching family
- configure interfage mode
- assign vlan to the interface

```
ge-0/0/0 {
    description "tf: Raspberry Pi";
    unit 0 {
        family ethernet-switching {
            interface-mode access;
            vlan {
                members VLAN_104;
            }
        }
    }
}
```

### MSTP

Standardized MSTP configuration file, no variables are needed as this should be copy/pasted across the fleet.

- MSTP configuration name
- MSTP bridge priority
- MSTP interfaces and their respective modes
- MSTI instance name
- VLANs associated to the MSTI instance

```
protocols {
    mstp {
        configuration-name brookefield;
        bridge-priority 32k;
        interface ge-0/0/11 {
            mode point-to-point;
        }
        interface all {
            edge;
        }
        msti 1 {
            vlan 1-4094;
        }
    }
}
```

## 📋 Terraform version compatibility

This project was tested with Terraform version v1.1.7

## 🚀 Deploy

```bash
terraform init
terraform plan
terraform apply
```

## Development

Want to contribute? Great!

Submit a PR and let's work on this together :D
