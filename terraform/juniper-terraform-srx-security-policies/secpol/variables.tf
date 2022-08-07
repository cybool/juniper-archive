
variable "apply_group_name" {
  type        = string
  description = "Name of our apply-group for the apply group stanza"
  // default     = "cdot65_sec_policy"
}


variable "from__zone__name" {
  type        = string
  description = "set security policy from zone {from__zone__name} to zone {to__zone__name}"
  // default     = "ZONE_UNTRUST"
}

variable "to__zone__name" {
  type        = string
  description = "set security policy from zone {from__zone__name} to zone {to__zone__name}"
  // default     = "ZONE_TRUST"
}

variable "policy_name" {
  type        = string
  description = "set security policy from zone {from__zone__name} to zone {to__zone__name} policy {policy_name}"
  // default     = "TF_SEC_POLICY1"
}

variable "description" {
  type        = string
  description = "set security policy from zone {from__zone__name} to zone {to__zone__name} policy {policy_name} description {description}"
  // default     = "Test Security Policy 1"
}

variable "application" {
  type        = string
  description = "set security policy from zone {from__zone__name} to zone {to__zone__name} policy {policy_name} match application {application}"
  // default     = "any"
}

variable "source__address" {
  type        = string
  description = "set security policy from zone {from__zone__name} to zone {to__zone__name} policy {policy_name} match source-address {source__address}"
  // default     = "any"
}

variable "destination__address" {
  type        = string
  description = "set security policy from zone {from__zone__name} to zone {to__zone__name} policy {policy_name} match destination-address {destination__address}"
  // default     = "any"
}

