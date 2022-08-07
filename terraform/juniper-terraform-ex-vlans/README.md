# Juniper Terraform Example: Configure VLANs

[![N|Solid](https://raw.githubusercontent.com/cdot65/juniper-terraform-srx/dev/site/content/assets/images/topology.png)](https://juniper.net/)

## Overview

The goal of this project is to provide an example method to interact with Juniper EX products with Terraform.

This project will build a VLAN configuration

- create vlan with a name of VLAN_103
- apply a description of `tf: VLAN 103 for devOps` to our new vlan
- associate a routed interface to this vlan

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
