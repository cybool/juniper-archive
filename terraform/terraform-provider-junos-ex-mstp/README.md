# Juniper Terraform Provider: EX MSTP

[![N|Solid](https://raw.githubusercontent.com/cdot65/juniper-terraform-srx/dev/site/content/assets/images/topology.png)](https://juniper.net/)

## Overview

The goal of this project is to provide an example method to interact with Juniper EX products with Terraform. We will be configuring the following:

```
/protocols/mstp/configuration-name
/protocols/mstp/bridge-priority
/protocols/mstp/interface/name
/protocols/mstp/interface/mode
/protocols/mstp/msti/name
/protocols/mstp/msti/vlan
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
