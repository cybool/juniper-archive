#!/usr/bin/python

# Copyright: (c) 2022, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible_collections.cdot65.mist.plugins.module_utils.mist.api import MistHelper  # pylint: disable=import-error


__metaclass__ = type  # pylint: disable=invalid-name

DOCUMENTATION = r"""
---
module: gateway

short_description: Manage configuration of gateways within your Mist organization.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description: This module will leverage Mist's REST API to automate the lifecycle management of your gateway configurations in Mist.

options:
    additional_config_cmds:
        description:
            - Junos configurations in "set" format
        required: false
        type: list

    api_token:
        description:
            - API token, used for authentication
            - can be stored as an environmental (MIST_API_KEY or MIST_API_TOKEN)
            - please consider using Ansible Vault or some other secure vault for this variable
        required: true
        type: str

    org_id:
        description:
            - your Mist Organization ID
            - can be found @ https://api.mist.com/api/v1/self
            - can leverage an environment of MIST_ORG_ID on your Ansible host
        required: true
        type: str

    role:
        description:
            - role for the gateway
        required: false
        type: str

    site_id:
        description:
            - id of the site
            - note: this is faster than using the site_name option
        required: false
        type: str

    site_name:
        description:
            - name of the site
            - note: this is slower than using the site_id option
            -   it requires an additional API lookup to find the site_id
        required: false
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - cdot65.mist.gateway

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
### #################################################################
### # Create the gateway
### #################################################################
        - name: "create a gateway configuration"
          cdot65.mist.gateway:
            # mist parameters
            baseurl: "{{ mist.url }}"
            api_token: "{{ mist.token }}"
            org_id: "{{ mist.org }}"

            # srx parameters
            name: "{{ gateway_hostname }}"
            site_name: "{{ site_name }}"
            bgp_config:
              - name: "ATT"
                type: "external"
                local_as: 42551
                auth_key: "juniper123"
                export_policy: "direct"
                neighbors:
                  - name: "74.51.192.0"
                    neighbor_as: 42550
                    export_policy: "direct"
                    import_policy: ""
            additional_config_cmds:
              - "set protocols bgp group ATT local-address 74.51.192.1"
            routing_policies:
              - name: "direct"
                terms:
                  - prefix: "10.0.0.0/8"
                    network: "Guest"
                    as_path: 0
                    protocol: "direct"
                    then: "accept"
                  - prefix: "10.0.0.0/8"
                    network: "IoT"
                    as_path: 0
                    protocol: "direct"
                    then: "accept"
                  - prefix: "10.0.0.0/8"
                    network: "Corporate"
                    as_path: 0
                    protocol: "direct"
                    then: "accept"
            service_policies:
              - name: "Corporate-Internet"
                tenants:
                  - "Corporate"
                services:
                  - "Corporate_Service"
                action: "allow"
                path_preference: "Internet"
"""


def core(module):
    """Main execution of our gateway Ansible module."""
    org_id = module.params["org_id"]
    rest = MistHelper(module)

    try:
        site_id = module.params["site_id"]
    except KeyError:
        site_id = None

    #########################################################################################################
    # Error the module out if a user didn't add a site_id or site_name
    #########################################################################################################
    if site_id is None:

        # Collect a list of the sites already present within the organization.
        response = rest.get(f"orgs/{org_id}/sites")
        if response.status_code != 200:
            module.fail_json(msg=f"Failed to receive information about the current sites, {response.info}")

        # Create a new object called 'sites' that will hold the sites returned from the API.
        sites = response.json

        # Validate that the objects 'sites' is in list format."""
        if isinstance(sites, list):
            pass
        else:
            module.fail_json(msg=f"The sites returned from the API are not in a list format: {sites}")

        # translate the site name to a site_id
        try:
            site_name = module.params["site_name"]
            site_id = ""
            for each in sites:
                if each["name"] == site_name:
                    site_id = each["id"]
        except KeyError:
            module.fail_json(msg=f"You need to pass either a site_id or site-name parameter: {response.info}")

        # fail task if a selected site does not exist in Mist
        if site_id == "":
            module.fail_json(msg=f"You selected a site that does not exist: {sites}")

    #########################################################################################################
    # gather a list of devices already created at the org-level
    #########################################################################################################
    response = rest.get(f"orgs/{org_id}/inventory?vc=true")
    if response.status_code != 200:
        module.fail_json(
            msg=f"Failed to receive information about the current inventory, here is the response information to help you debug : {response.info}"
        )

    #########################################################################################################
    # save the output of our API call to a new object called sites
    #########################################################################################################
    inventory = response.json

    #########################################################################################################
    # check to see if the inventory object is a list, fail the module if the return payload is anything else
    #########################################################################################################
    if isinstance(inventory, list):
        pass
    else:
        module.fail_json(
            msg=f"The inventory returned from the API are not in a list format, contant Mist support: {inventory}"
        )

    #########################################################################################################
    # create a new dictionary with a k/v of 'provisioned' set to False. if the gateway has already been
    # provisioned, we'll flip this bit to True and store it's gateway ID
    #########################################################################################################
    gateway = dict()
    gateway["provisioned"] = False
    gateway["id"] = None
    for each in inventory:
        if each["type"] == "gateway":
            try:
                if each["name"] == module.params["name"]:
                    gateway["provisioned"] = True
                    gateway["id"] = each["id"]
            except KeyError:
                pass

    #########################################################################################################
    # create an empty object to store configuration parameters, fed to it in the Ansible Module's parameters.
    # this is the python dictionary that will be converted to JSON before pushing to the Mist API.
    #########################################################################################################
    gateway_config = dict()

    #########################################################################################################
    # set the key/value pairs of the Ansible module parameters to a new object called `parameters`.
    # iterate over the object, look to see if anything was entered and append it to our empty dict
    #########################################################################################################
    parameters = module.params.items()
    for key, value in parameters:
        if value is not None:
            gateway_config[key] = value

    #########################################################################################################
    # pop off unnessesary baggage, we do not want this information posted to the API.
    #########################################################################################################
    gateway_config.pop("api_token")
    gateway_config.pop("org_id")
    try:
        gateway_config.pop("site_id")
    except KeyError:
        pass

    #########################################################################################################
    # change up some of the parameters to make it Mist API friendly:
    #   - networks will be translated from a list into a dictionary.
    # this is to address the fact that the API uses the name of a network as the key, and that's simply
    # impossible to address as an Ansible argument spect
    #########################################################################################################
    if "bgp_config" in gateway_config:
        bgp_groups_config = dict()

        for each in gateway_config["bgp_config"]:
            bgp_group = dict()
            bgp_group[each["name"]] = dict()
            bgp_group[each["name"]]["type"] = each["type"]
            bgp_group[each["name"]]["local_as"] = each["local_as"]
            bgp_group[each["name"]]["auth_key"] = each["auth_key"]
            bgp_group[each["name"]]["neighbors"] = dict()
            for neighbor in each["neighbors"]:
                bgp_group[each["name"]]["neighbors"][neighbor["name"]] = dict()
                bgp_group[each["name"]]["neighbors"][neighbor["name"]]["neighbor_as"] = neighbor["neighbor_as"]
                bgp_group[each["name"]]["neighbors"][neighbor["name"]]["export"] = neighbor["export_policy"]
                bgp_group[each["name"]]["neighbors"][neighbor["name"]]["import"] = neighbor["import_policy"]
            bgp_group[each["name"]]["export"] = each["export_policy"]
            bgp_groups_config.update(bgp_group)

        gateway_config["bgp_config"] = bgp_groups_config

    #########################################################################################################
    # same as the situation above for routing_policies.
    #########################################################################################################
    if "routing_policies" in gateway_config:
        routing_policies_config = list()
        for each in gateway_config["routing_policies"]:
            policy_config = dict()
            policy_config[each["name"]] = dict()
            policy_config[each["name"]]["terms"] = list()
            for each_term in each["terms"]:
                term_config = dict()
                term_config["prefix"] = each_term["prefix"]
                term_config["network"] = each_term["network"]
                term_config["as_path"] = each_term["as_path"]
                term_config["protocol"] = each_term["protocol"]
                term_config["then"] = each_term["then"]
                policy_config[each["name"]]["terms"].append(term_config)

            routing_policies_config.append(policy_config)

        gateway_config["routing_policies"] = routing_policies_config

    #########################################################################################################
    # so, here we meet again. same issue, this time for port_profiles
    #########################################################################################################
    if "service_policies" in gateway_config:
        friendly_port_profiles = dict()
        # for each in gateway_config["port_profiles"]:
        #     port_profile = dict()
        #     port_profile[each["name"]] = dict()
        #     port_profile[each["name"]]["all_networks"] = each["all_networks"]
        #     port_profile[each["name"]]["disabled"] = each["disabled"]
        #     port_profile[each["name"]]["duplex"] = each["duplex"]
        #     port_profile[each["name"]]["mac_limit"] = each["mac_limit"]
        #     port_profile[each["name"]]["mode"] = each["mode"]
        #     port_profile[each["name"]]["name"] = each["name"]
        #     port_profile[each["name"]]["networks"] = each["networks"]
        #     port_profile[each["name"]]["poe_disabled"] = each["poe_disabled"]
        #     port_profile[each["name"]]["port_auth"] = each["port_auth"]
        #     port_profile[each["name"]]["port_network"] = each["port_network"]
        #     port_profile[each["name"]]["speed"] = each["speed"]
        #     port_profile[each["name"]]["stp_edge"] = each["stp_edge"]
        #     port_profile[each["name"]]["voip_network"] = each["voip_network"]
        #     friendly_port_profiles.update(port_profile)

        gateway_config["service_policies"] = friendly_port_profiles

    #########################################################################################################
    # finally, we will add some defaults to each SRX gateway config.
    #########################################################################################################
    gateway_config["cliConfigExists"] = True
    gateway_config["disable_auto_config"] = False
    gateway_config["-extra_routes"] = True
    gateway_config["-path_preferences"] = True
    gateway_config["-dhcpd_config"] = True
    gateway_config["-ip_configs"] = True
    gateway_config["-port_config"] = True

    #########################################################################################################
    # create our Gateway configuration.
    #########################################################################################################
    if gateway["provisioned"] is False:
        module.exit_json(changed=False, data="Device was not found, exiting")
    else:
        response = rest.put(f"/sites/{site_id}/devices/{gateway['id']}", data=gateway_config)
        module.exit_json(changed=True, data=response.json)


def main():
    """Define data model and Ansible module objects and pass them into our core function."""

    # create a new object based on our data model for gateways defined in MistHelper.
    gateway_spec = MistHelper.gateway_spec()

    # pass our gateway_spec into AnsibleModule's argument_spec, save object as 'module'.
    gateway_module = AnsibleModule(argument_spec=gateway_spec)

    # pass our module into the `core` function, fail gracefully if an error shows up.
    try:
        core(gateway_module)
    except Exception as e:
        gateway_module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    """Execution of our gateway module."""
    main()
