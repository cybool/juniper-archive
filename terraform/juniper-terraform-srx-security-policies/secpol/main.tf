terraform {
  required_providers {
    junos-security-policies = {
      source  = "cdot65/junos-security-policies"
      version = "0.0.1"
    }
  }
}

// Policy Description
resource "junos-security-policies_SecurityPoliciesPolicyPolicyDescription" "policy_description" {
  resource_name    = format("%s_%s", var.apply_group_name, "description")
  name             = var.policy_name
  from__zone__name = var.from__zone__name
  to__zone__name   = var.to__zone__name
  description      = var.description
}

// Match application
resource "junos-security-policies_SecurityPoliciesPolicyPolicyMatchApplication" "policy_match_application" {
  resource_name    = format("%s_%s", var.apply_group_name, "match_application")
  name             = var.policy_name
  from__zone__name = var.from__zone__name
  to__zone__name   = var.to__zone__name
  application      = var.application
}

// Match destination address
resource "junos-security-policies_SecurityPoliciesPolicyPolicyMatchDestination__Address" "policy_match_dst_addr" {
  resource_name        = format("%s_%s", var.apply_group_name, "match_dst_addr")
  name                 = var.policy_name
  from__zone__name     = var.from__zone__name
  to__zone__name       = var.to__zone__name
  destination__address = var.destination__address
}

// Match source address
resource "junos-security-policies_SecurityPoliciesPolicyPolicyMatchSource__Address" "policy_match_src_addr" {
  resource_name    = format("%s_%s", var.apply_group_name, "match_src_addr")
  name             = var.policy_name
  from__zone__name = var.from__zone__name
  to__zone__name   = var.to__zone__name
  source__address  = var.source__address
}

// Then Count
resource "junos-security-policies_SecurityPoliciesPolicyPolicyThenCount" "policy_then_count" {
  resource_name    = format("%s_%s", var.apply_group_name, "then_count")
  name             = var.policy_name
  from__zone__name = var.from__zone__name
  to__zone__name   = var.to__zone__name
}

// Then Permit
resource "junos-security-policies_SecurityPoliciesPolicyPolicyThenPermit" "policy_then_permit" {
  resource_name    = format("%s_%s", var.apply_group_name, "then_permit")
  name             = var.policy_name
  from__zone__name = var.from__zone__name
  to__zone__name   = var.to__zone__name
}
