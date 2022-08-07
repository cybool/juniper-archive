# Juniper Terraform Example: Configure Interfaces

[![N|Solid](https://raw.githubusercontent.com/cdot65/juniper-terraform-srx/dev/site/content/assets/images/topology.png)](https://juniper.net/)

## Overview

The goal of this project is to provide an example method to interact with Juniper SRX products with Terraform.

This project will build an interface configuration on a Juniper SRX firewall

- create interface `ge-0/0/0`
- apply a description of `tf: Raspberry Pi` to our new interface
- create a sub-interface of `ge-0/0/0` with a unit ID of `0`
- set interface `ge-0/0/0.0` to ethernet-switching family
- configure interfage `ge-0/0/0.0` in access mode
- assign vlan `VLAN_104` to the interface

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
