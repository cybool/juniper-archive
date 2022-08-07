# Juniper Terraform Example: SRX security policies

[![N|Solid](https://raw.githubusercontent.com/cdot65/juniper-terraform-srx/dev/site/content/assets/images/topology.png)](https://juniper.net/)

## Overview

The goal of this project is to provide an example method to interact with Juniper SRX products with Terraform.

This project will manage SRX security policies.

## 📋 Terraform version compatibility

This project was tested with Terraform version v1.1.7

## 🚀 Deploy

```bash
terraform init
terraform plan
terraform apply
```

Resulting configuration in configuration groups, revealed by asking for inherited configuration

```sql
[edit]
cdot@hdq-dfw-001# show security policies | display set | display inheritance
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY1 description "Security Policy 1"
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY1 match source-address any
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY1 match destination-address any
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY1 match application any
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY1 then permit
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY1 then count
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY2 description "Security Policy 2"
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY2 match source-address any
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY2 match destination-address any
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY2 match application any
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY2 then permit
set security policies from-zone ZONE_TRUST to-zone ZONE_UNTRUST policy TF_SEC_POLICY2 then count
```

## Development

Want to contribute? Great!

Submit a PR and let's work on this together :D
