"""Apstra Rest API SDK."""
# Copyright: (c) 2022, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import json
from ansible.module_utils.urls import fetch_url  # pylint: disable=import-error
from ansible.module_utils._text import to_text  # pylint: disable=import-error
from ansible.module_utils.basic import env_fallback  # pylint: disable=import-error

__metaclass__ = type  # pylint: disable=invalid-name


class Response(object):
    """Custom handling of response object."""

    def __init__(self, resp, info):
        self.body = None
        if resp:
            self.body = resp.read()
        self.info = info

    @property
    def json(self):
        """Return JSON object."""
        if not self.body:
            if "body" in self.info:
                return json.loads(to_text(self.info["body"]))
            return None
        try:
            return json.loads(to_text(self.body))
        except ValueError:
            return None

    @property
    def status_code(self):
        """Return status code."""
        return self.info["status"]


class ApstraHelper:
    """Map out method of interacting with Apstra's REST API."""

    def __init__(self, module):
        self.module = module
        self.server = module.params.get("server")
        self.validate_certs = module.params.get("validate_certs", False)
        self.baseurl = f"https://{self.server}/api"
        self.timeout = module.params.get("timeout", 30)
        self.api_token = module.params.get("api_token")
        self.headers = {
            "AUTHTOKEN": f"{self.api_token}",
            "Content-type": "application/json",
            "accept": "application/json",
        }

        # Check if api_token is valid or not by testing the blueprints url
        response = self.get("blueprints")
        if response.status_code == 401:
            self.module.fail_json(
                msg="Failed to login using API token, verify token.")

    def _url_builder(self, path):
        """Strip off trailing / within URI."""
        if path[0] == "/":
            path = path[1:]
        return f"{self.baseurl}/{path}"

    def send(self, method, path, data=None):
        """Handle the sending of API calls."""
        url = self._url_builder(path)
        data = self.module.jsonify(data)

        resp, info = fetch_url(
            self.module,
            url,
            data=data,
            headers=self.headers,
            method=method,
            timeout=self.timeout,
        )

        return Response(resp, info)

    def get(self, path, data=None):
        """HTTP GET method."""
        return self.send("GET", path, data)

    def put(self, path, data=None):
        """HTTP PUT method."""
        return self.send("PUT", path, data)

    def post(self, path, data=None):
        """HTTP POST method."""
        return self.send("POST", path, data)

    def delete(self, path, data=None):
        """HTTP DELETE method."""
        return self.send("DELETE", path, data)

    @staticmethod
    def blueprint_spec():
        """Define the data model for Blueprints."""
        return dict(
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_API_TOKEN", "APSTRA_API_TOKEN", "API_TOKEN"],
                ),
                no_log=True,
                type="str",
            ),
            design=dict(required=False, type="str"),
            id=dict(required=True, type="str"),
            init_type=dict(required=False, type="str"),
            label=dict(required=True, type="str"),
            template_id=dict(required=False, type="str"),
            port=dict(required=False, type="int"),
            server=dict(required=False, type="str"),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            validate_certs=dict(type="bool", required=False, default=False),
        )

    @staticmethod
    def device_profiles_spec():
        """Defined the data model for Device Profiles."""
        return dict(
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_API_TOKEN", "APSTRA_API_TOKEN", "API_TOKEN"],
                ),
                no_log=True,
                type="str",
            ),
            hardware_capabilities=dict(
                required=False,
                type="dict",
                options=dict(
                    userland=dict(required=False, type="int"),
                    ram=dict(required=False, type="int"),
                    asic=dict(required=False, type="str"),
                    form_factor=dict(required=False, type="str"),
                    ecmp_limit=dict(required=False, type="int"),
                    cpu=dict(required=False, type="str"),
                    routing_instance_supported=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            version=dict(
                                required=True,
                                type="str",
                            ),
                            value=dict(
                                required=True,
                                type="bool",
                            ),
                        ),
                    ),
                ),
            ),
            id=dict(required=False, type="str"),
            label=dict(required=True, type="str"),
            ports=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    port_id=dict(
                        required=True,
                        type="int",
                    ),
                    slot_id=dict(
                        required=True,
                        type="int",
                    ),
                    panel_id=dict(
                        required=True,
                        type="int",
                    ),
                    connector_type=dict(
                        required=True,
                        type="str",
                    ),
                    failure_domain_id=dict(
                        required=True,
                        type="int",
                    ),
                    row_id=dict(
                        required=True,
                        type="int",
                    ),
                    column_id=dict(
                        required=True,
                        type="int",
                    ),
                    transformations=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            transformation_id=dict(required=False, type="int"),
                            is_default=dict(required=False, type="bool"),
                            interfaces=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    interface_id=dict(
                                        required=False, type="int"),
                                    name=dict(required=False, type="str"),
                                    state=dict(required=False, type="str"),
                                    speed=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=False, type="str"),
                                            value=dict(
                                                required=False, type="int"),
                                        ),
                                    ),
                                    setting=dict(required=False, type="str"),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            selector=dict(
                required=False,
                type="dict",
                options=dict(
                    os_version=dict(required=False, type="str"),
                    model=dict(required=False, type="str"),
                    os=dict(required=False, type="str"),
                    manufacturer=dict(required=False, type="str"),
                ),
            ),
            slot_count=dict(required=False, type="int"),
            software_capabilities=dict(
                required=False,
                type="dict",
                options=dict(
                    onie=dict(required=False, type="bool"),
                    config_apply_support=dict(required=False, type="str"),
                    lxc_support=dict(required=False, type="bool"),
                ),
            ),
            server=dict(required=False, type="str"),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            validate_certs=dict(type="bool", required=False, default=False),
        )

    @staticmethod
    def resources_spec():
        """Defined the data model for the various Resources."""
        return dict(
            address=dict(required=False, type="str"),
            asn=dict(required=False, type="int"),
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_API_TOKEN", "APSTRA_API_TOKEN", "API_TOKEN"],
                ),
                no_log=True,
                type="str",
            ),
            display_name=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_USERNAME", "APSTRA_USERNAME", "USERNAME"],
                ),
                type="str",
            ),
            id=dict(required=True, type="str"),
            ipv6_address=dict(required=False, type="str"),
            port=dict(required=False, type="int"),
            ranges=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    first=dict(required=True, type="int"),
                    last=dict(required=True, type="int"),
                ),
            ),
            server=dict(required=False, type="str"),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            subnets=dict(required=False, type="list", elements="str"),
            tags=dict(required=False, type="list", elements="str"),
            type=dict(
                required=True,
                choices=[
                    "asn-pools",
                    "external-routers",
                    "ip-pools",
                    "ipv6-pools",
                    "vlan-pools",
                    "vni-pools",
                ],
                type="str",
            ),
            validate_certs=dict(type="bool", required=False, default=False),
        )

    @staticmethod
    def design_spec():
        """Defined the data model for Design."""
        return dict(
            access_switches=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    access_access_link_count=dict(
                        required=True,
                        type="int",
                    ),
                    access_access_link_speed=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            unit=dict(
                                required=True,
                                type="str",
                            ),
                            value=dict(
                                required=True,
                                type="int",
                            ),
                        ),
                    ),
                    instance_count=dict(
                        required=True,
                        type="int",
                    ),
                    label=dict(
                        required=True,
                        type="str",
                    ),
                    links=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            attachment_type=dict(
                                required=False,
                                type="str",
                            ),
                            label=dict(
                                required=False,
                                type="str",
                            ),
                            lag_mode=dict(
                                required=False,
                                type="str",
                            ),
                            link_per_switch_count=dict(
                                required=False,
                                type="int",
                            ),
                            link_speed=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    unit=dict(
                                        required=True,
                                        type="str",
                                    ),
                                    value=dict(
                                        required=True,
                                        type="int",
                                    ),
                                ),
                            ),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                            target_switch_label=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                    ),
                    logical_device=dict(
                        required=True,
                        type="str",
                    ),
                    redundancy_protocol=dict(
                        required=True,
                        type="str",
                    ),
                    tags=dict(required=True, type="list", elements="str"),
                ),
            ),
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_API_TOKEN", "APSTRA_API_TOKEN", "API_TOKEN"],
                ),
                no_log=True,
                type="str",
            ),
            description=dict(required=False, type="str"),
            device_profile_id=dict(required=False, type="str"),
            display_name=dict(
                required=False,
                fallback=(
                    env_fallback,
                    ["APSTRA_USERNAME", "APSTRA_USERNAME", "USERNAME"],
                ),
                type="str",
            ),
            fabric_connectivity_design=dict(required=False, type="str"),
            generic_systems=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    asn_domain=dict(
                        required=True,
                        type="str",
                    ),
                    count=dict(
                        required=True,
                        type="int",
                    ),
                    label=dict(
                        required=True,
                        type="str",
                    ),
                    links=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            attachment_type=dict(
                                required=False,
                                type="str",
                            ),
                            label=dict(
                                required=False,
                                type="str",
                            ),
                            lag_mode=dict(
                                required=False,
                                type="str",
                            ),
                            leaf_peer=dict(required=False, type="str"),
                            link_per_switch_count=dict(
                                required=False,
                                type="int",
                            ),
                            link_speed=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    unit=dict(
                                        required=True,
                                        type="str",
                                    ),
                                    value=dict(
                                        required=True,
                                        type="int",
                                    ),
                                ),
                            ),
                            switch_peer=dict(required=False, type="str"),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                            target_switch_label=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                    ),
                    logical_device=dict(
                        required=True,
                        type="str",
                    ),
                    loopback=dict(
                        required=True,
                        type="str",
                    ),
                    management_level=dict(
                        required=True,
                        type="str",
                    ),
                    port_channel_id_max=dict(
                        required=True,
                        type="int",
                    ),
                    port_channel_id_min=dict(
                        required=True,
                        type="int",
                    ),
                    tags=dict(required=True, type="list", elements="str"),
                ),
            ),
            id=dict(required=False, type="str"),
            interfaces=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    mapping=dict(required=True, type="list", elements="int"),
                    name=dict(
                        required=True,
                        type="str",
                    ),
                    position=dict(
                        required=True,
                        type="int",
                    ),
                    roles=dict(required=True, type="list", elements="str"),
                    setting=dict(
                        required=True,
                        type="dict",
                        options=dict(
                            param=dict(required=False, type="str"),
                        ),
                    ),
                    speed=dict(
                        required=True,
                        type="dict",
                        options=dict(
                            unit=dict(required=False, type="str"),
                            value=dict(required=False, type="int"),
                        ),
                    ),
                    state=dict(
                        required=True,
                        type="str",
                    ),
                ),
            ),
            label=dict(required=False, type="str"),
            leafs=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    label=dict(
                        required=False,
                        type="str",
                    ),
                    leaf_leaf_l3_link_count=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_l3_link_port_channel_id=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_l3_link_speed=dict(
                        required=False,
                        type="str",
                    ),
                    leaf_leaf_link_count=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_link_port_channel_id=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_link_speed=dict(
                        required=False,
                        type="str",
                    ),
                    link_per_spine_count=dict(
                        required=False,
                        type="int",
                    ),
                    link_per_spine_speed=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            unit=dict(required=False, type="str"),
                            value=dict(required=False, type="int"),
                        ),
                    ),
                    logical_device=dict(
                        required=False,
                        type="str",
                    ),
                    redundancy_protocol=dict(
                        required=False,
                        type="str",
                    ),
                    tags=dict(required=True, type="list", elements="str"),
                ),
            ),
            logical_devices=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    display_name=dict(
                        required=True,
                        type="str",
                    ),
                    id=dict(
                        required=True,
                        type="str",
                    ),
                    panels=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            panel_layout=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    row_count=dict(required=False, type="int"),
                                    column_count=dict(
                                        required=False, type="int"),
                                ),
                            ),
                            port_indexing=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    order=dict(required=False, type="str"),
                                    start_index=dict(
                                        required=False, type="int"),
                                    schema=dict(required=False, type="str"),
                                ),
                            ),
                            port_groups=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    count=dict(required=False, type="int"),
                                    roles=dict(required=False,
                                               type="list", elements="str"),
                                    speed=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=False, type="str"),
                                            value=dict(
                                                required=False, type="int"),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            logical_device_id=dict(required=False, type="str"),
            name=dict(required=False, type="str"),
            panels=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    panel_layout=dict(
                        required=True,
                        type="dict",
                        options=dict(
                            row_count=dict(required=False, type="int"),
                            column_count=dict(required=False, type="int"),
                        ),
                    ),
                    port_indexing=dict(
                        required=True,
                        type="dict",
                        options=dict(
                            order=dict(required=False, type="str"),
                            schema=dict(required=False, type="str"),
                            start_index=dict(required=False, type="int"),
                        ),
                    ),
                    port_groups=dict(
                        required=True,
                        type="list",
                        elements="dict",
                        options=dict(
                            count=dict(required=False, type="int"),
                            roles=dict(required=False, type="list",
                                       elements="str"),
                            speed=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    value=dict(required=False, type="int"),
                                    unit=dict(required=False, type="str"),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            port=dict(required=False, type="int"),
            server=dict(required=False, type="str"),
            servers=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    connectivity_type=dict(
                        required=True,
                        type="str",
                    ),
                    count=dict(
                        required=True,
                        type="int",
                    ),
                    label=dict(
                        required=True,
                        type="str",
                    ),
                    logical_device=dict(
                        required=True,
                        type="str",
                    ),
                    ip_version=dict(
                        required=True,
                        type="str",
                    ),
                    port_channel_id_min=dict(
                        required=True,
                        type="int",
                    ),
                    port_channel_id_max=dict(
                        required=True,
                        type="int",
                    ),
                    links=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            attachment_type=dict(required=False, type="str"),
                            label=dict(required=False, type="str"),
                            lag_mode=dict(required=False, type="str"),
                            leaf_peer=dict(required=False, type="str"),
                            link_per_switch_count=dict(
                                required=False, type="int"),
                            link_speed=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    unit=dict(required=False, type="str"),
                                    value=dict(required=False, type="int"),
                                ),
                            ),
                            target_switch_label=dict(
                                required=False, type="str"),
                        ),
                    ),
                ),
            ),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            design_template=dict(
                required=False,
                type="dict",
                options=dict(
                    asn_allocation_policy=dict(
                        required=False,
                        type="dict",
                        options=dict(spine_asn_scheme=dict(
                            required=False, type="str")),
                    ),
                    dhcp_service_intent=dict(
                        required=False,
                        type="dict",
                        options=dict(active=dict(required=False, type="bool")),
                    ),
                    display_name=dict(required=True, type="str"),
                    external_routing_policy=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            export_policy=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    all_routes=dict(
                                        required=False, type="bool"),
                                    l2edge_subnets=dict(
                                        required=False, type="bool"),
                                    l3edge_server_links=dict(
                                        required=False, type="bool"),
                                    loopbacks=dict(
                                        required=False, type="bool"),
                                    spine_leaf_links=dict(
                                        required=False, type="bool"),
                                    static_routes=dict(
                                        required=False, type="bool"),
                                ),
                            ),
                            import_policy=dict(required=False, type="str"),
                        ),
                    ),
                    fabric_addressing_policy=dict(
                        required=False,
                        type="dict",
                        options=dict(spine_leaf_links=dict(
                            required=False, type="str")),
                    ),
                    id=dict(required=False, type="str"),
                    rack_type_counts=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            count=dict(required=False, type="int"),
                            rack_type_id=dict(required=False, type="str"),
                        ),
                    ),
                    rack_types=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            access_switches=dict(
                                required=False, type="list", elements="str"),
                            description=dict(required=False, type="str"),
                            display_name=dict(required=False, type="str"),
                            fabric_connectivity_design=dict(
                                required=False, type="str"),
                            generic_systems=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    asn_domain=dict(
                                        required=False, type="str"),
                                    count=dict(required=False, type="int"),
                                    label=dict(required=False, type="str"),
                                    links=dict(
                                        required=False,
                                        type="list",
                                        elements="dict",
                                        options=dict(
                                            attachment_type=dict(
                                                required=False, type="str"),
                                            label=dict(
                                                required=False, type="str"),
                                            lag_mode=dict(
                                                required=False, type="str"),
                                            link_per_switch_count=dict(
                                                required=False, type="int"),
                                            link_speed=dict(
                                                required=True,
                                                type="dict",
                                                options=dict(
                                                    unit=dict(
                                                        required=False, type="str"),
                                                    value=dict(
                                                        required=False, type="int"),
                                                ),
                                            ),
                                            tags=dict(
                                                required=False,
                                                type="list",
                                                elements="str",
                                            ),
                                            target_switch_label=dict(
                                                required=False, type="str"),
                                        ),
                                    ),
                                    logical_device=dict(
                                        required=False, type="str"),
                                    loopback=dict(required=False, type="str"),
                                    management_level=dict(
                                        required=False, type="str"),
                                    port_channel_id_max=dict(
                                        required=False, type="int"),
                                    port_channel_id_min=dict(
                                        required=False, type="int"),
                                    tags=dict(required=False,
                                              type="list", elements="str"),
                                ),
                            ),
                            id=dict(required=False, type="str"),
                            leafs=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    label=dict(required=False, type="str"),
                                    leaf_leaf_l3_link_count=dict(
                                        required=False, type="int"),
                                    leaf_leaf_l3_link_port_channel_id=dict(
                                        required=False, type="int"),
                                    leaf_leaf_l3_link_speed=dict(
                                        required=False, type="str"),
                                    leaf_leaf_link_count=dict(
                                        required=False, type="int"),
                                    leaf_leaf_link_port_channel_id=dict(
                                        required=False, type="int"),
                                    leaf_leaf_link_speed=dict(
                                        required=False, type="str"),
                                    link_per_spine_count=dict(
                                        required=False, type="int"),
                                    link_per_spine_speed=dict(
                                        required=False,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                type="str", required=False),
                                            value=dict(
                                                type="int", required=False),
                                        ),
                                    ),
                                    logical_device=dict(
                                        required=True, type="str"),
                                    redundancy_protocol=dict(
                                        required=False, type="str"),
                                    tags=dict(required=False,
                                              type="list", elements="str"),
                                ),
                            ),
                            logical_devices=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    display_name=dict(
                                        required=True, type="str"),
                                    id=dict(required=True, type="str"),
                                    panels=dict(
                                        required=False,
                                        type="list",
                                        elements="dict",
                                        options=dict(
                                            panel_layout=dict(
                                                required=False,
                                                type="dict",
                                                options=dict(
                                                    column_count=dict(
                                                        required=False, type="int"),
                                                    row_count=dict(
                                                        required=False, type="int"),
                                                ),
                                            ),
                                            port_groups=dict(
                                                required=False,
                                                type="list",
                                                elements="dict",
                                                options=dict(
                                                    count=dict(
                                                        required=False, type="int"),
                                                    roles=dict(
                                                        required=False,
                                                        type="list",
                                                        elements="str",
                                                    ),
                                                    speed=dict(
                                                        required=False,
                                                        type="dict",
                                                        options=dict(
                                                            unit=dict(
                                                                required=False,
                                                                type="str",
                                                            ),
                                                            value=dict(
                                                                required=False,
                                                                type="int",
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            port_indexing=dict(
                                                required=True,
                                                type="dict",
                                                options=dict(
                                                    order=dict(
                                                        required=True, type="str"),
                                                    schema=dict(
                                                        required=True, type="str"),
                                                    start_index=dict(
                                                        required=True, type="int"),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                            servers=dict(
                                required=True,
                                type="list",
                                elements="dict",
                                options=dict(
                                    connectivity_type=dict(
                                        type="str", required=True),
                                    count=dict(type="int", required=True),
                                    ip_version=dict(type="str", required=True),
                                    label=dict(type="str", required=True),
                                    links=dict(
                                        required=True,
                                        type="list",
                                        elements="dict",
                                        options=dict(
                                            attachment_type=dict(
                                                type="str", required=True),
                                            label=dict(
                                                type="str", required=True),
                                            lag_mode=dict(
                                                type="str", required=False),
                                            link_per_switch_count=dict(
                                                type="int", required=False),
                                            link_speed=dict(
                                                required=True,
                                                type="dict",
                                                options=dict(
                                                    unit=dict(
                                                        type="str", required=False),
                                                    value=dict(
                                                        type="int", required=False),
                                                ),
                                            ),
                                            target_switch_label=dict(
                                                type="str", required=True),
                                        ),
                                    ),
                                    logical_device=dict(
                                        type="str", required=True),
                                    port_channel_id_max=dict(
                                        type="int", required=False),
                                    port_channel_id_min=dict(
                                        type="int", required=False),
                                ),
                            ),
                            tags=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    description=dict(
                                        required=False, type="str"),
                                    label=dict(required=False, type="str"),
                                ),
                            ),
                        ),
                    ),
                    spine=dict(
                        required=True,
                        type="dict",
                        options=dict(
                            count=dict(required=True, type="int"),
                            link_per_superspine_count=dict(
                                required=True, type="int"),
                            link_per_superspine_speed=dict(
                                required=True, type="str"),
                            logical_device=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    display_name=dict(
                                        required=True, type="str"),
                                    id=dict(required=True, type="str"),
                                    panels=dict(
                                        required=False,
                                        type="list",
                                        elements="dict",
                                        options=dict(
                                            panel_layout=dict(
                                                required=False,
                                                type="dict",
                                                options=dict(
                                                    column_count=dict(
                                                        required=False, type="int"),
                                                    row_count=dict(
                                                        required=False, type="int"),
                                                ),
                                            ),
                                            port_groups=dict(
                                                required=False,
                                                type="list",
                                                elements="dict",
                                                options=dict(
                                                    count=dict(
                                                        required=False, type="int"),
                                                    roles=dict(
                                                        required=False,
                                                        type="list",
                                                        elements="str",
                                                    ),
                                                    speed=dict(
                                                        required=False,
                                                        type="dict",
                                                        options=dict(
                                                            unit=dict(
                                                                required=False,
                                                                type="str",
                                                            ),
                                                            value=dict(
                                                                required=False,
                                                                type="int",
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            port_indexing=dict(
                                                required=False,
                                                type="dict",
                                                options=dict(
                                                    order=dict(
                                                        type="str", required=False),
                                                    schema=dict(
                                                        type="str", required=False),
                                                    start_index=dict(
                                                        type="int", required=False),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                            tags=dict(required=False, type="list",
                                      elements="str"),
                        ),
                    ),
                    type=dict(required=True, type="str"),
                    virtual_network_policy=dict(
                        required=True,
                        type="dict",
                        options=dict(overlay_control_protocol=dict(
                            required=True, type="str")),
                    ),
                ),
            ),
            tags=dict(
                required=False,
                type="list",
                elements="str",
            ),
            type=dict(
                required=True,
                choices=[
                    "device-profiles",
                    "logical-devices",
                    "interface-maps",
                    "rack-types",
                    "templates",
                ],
                type="str",
            ),
            validate_certs=dict(type="bool", required=False, default=False),
        )

    @staticmethod
    def rack_spec():
        """Defined the data model for creating a new rack type."""
        return dict(
            access_switches=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    access_access_link_count=dict(
                        required=True,
                        type="int",
                    ),
                    access_access_link_speed=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            unit=dict(
                                required=True,
                                type="str",
                            ),
                            value=dict(
                                required=True,
                                type="int",
                            ),
                        ),
                    ),
                    instance_count=dict(
                        required=True,
                        type="int",
                    ),
                    label=dict(
                        required=True,
                        type="str",
                    ),
                    links=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            attachment_type=dict(
                                required=False,
                                type="str",
                            ),
                            label=dict(
                                required=False,
                                type="str",
                            ),
                            lag_mode=dict(
                                required=False,
                                type="str",
                            ),
                            link_per_switch_count=dict(
                                required=False, type="int"),
                            link_speed=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    unit=dict(
                                        required=True,
                                        type="str",
                                    ),
                                    value=dict(
                                        required=True,
                                        type="int",
                                    ),
                                ),
                            ),
                            # tags=dict(required=True, type="list",
                            #           elements="str"),
                            target_switch_label=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                    ),
                    logical_device=dict(
                        required=True,
                        type="str",
                    ),
                    redundancy_protocol=dict(
                        required=True,
                        type="str",
                    ),
                    # tags=dict(required=True, type="list", elements="str"),
                ),
            ),
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_API_TOKEN", "APSTRA_API_TOKEN", "API_TOKEN"],
                ),
                no_log=True,
                type="str",
            ),
            description=dict(required=False, type="str"),
            display_name=dict(
                required=False,
                type="str",
            ),
            fabric_connectivity_design=dict(required=True, type="str"),
            generic_systems=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    asn_domain=dict(
                        required=True,
                        type="str",
                    ),
                    count=dict(
                        required=True,
                        type="int",
                    ),
                    label=dict(
                        required=True,
                        type="str",
                    ),
                    links=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            attachment_type=dict(
                                required=False,
                                type="str",
                            ),
                            label=dict(
                                required=False,
                                type="str",
                            ),
                            lag_mode=dict(
                                required=False,
                                type="str",
                            ),
                            link_per_switch_count=dict(
                                required=False,
                                type="int",
                            ),
                            link_speed=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    unit=dict(
                                        required=True,
                                        type="str",
                                    ),
                                    value=dict(
                                        required=True,
                                        type="int",
                                    ),
                                ),
                            ),
                            switch_peer=dict(required=False, type="str"),
                            tags=dict(required=False, type="list",
                                      elements="str"),
                            target_switch_label=dict(
                                required=False,
                                type="str",
                            ),
                        ),
                    ),
                    logical_device=dict(
                        required=True,
                        type="str",
                    ),
                    loopback=dict(
                        required=True,
                        type="str",
                    ),
                    management_level=dict(
                        required=True,
                        type="str",
                    ),
                    port_channel_id_max=dict(
                        required=True,
                        type="int",
                    ),
                    port_channel_id_min=dict(
                        required=True,
                        type="int",
                    ),
                    tags=dict(required=True, type="list", elements="str"),
                ),
            ),
            id=dict(required=False, type="str"),
            leafs=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    label=dict(
                        required=False,
                        type="str",
                    ),
                    leaf_leaf_l3_link_count=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_l3_link_port_channel_id=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_l3_link_speed=dict(
                        required=False,
                        type="str",
                    ),
                    leaf_leaf_link_count=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_link_port_channel_id=dict(
                        required=False,
                        type="int",
                    ),
                    leaf_leaf_link_speed=dict(
                        required=False,
                        type="str",
                    ),
                    link_per_spine_count=dict(
                        required=False,
                        type="int",
                    ),
                    logical_device=dict(
                        required=False,
                        type="str",
                    ),
                    redundancy_protocol=dict(
                        required=False,
                        type="str",
                    ),
                    # tags=dict(required=True, type="list", elements="str"),
                ),
            ),
            logical_devices=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    display_name=dict(
                        required=True,
                        type="str",
                    ),
                    id=dict(
                        required=True,
                        type="str",
                    ),
                    panels=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            panel_layout=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    row_count=dict(required=False, type="int"),
                                    column_count=dict(
                                        required=False, type="int"),
                                ),
                            ),
                            port_indexing=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    order=dict(required=False, type="str"),
                                    start_index=dict(
                                        required=False, type="int"),
                                    schema=dict(required=False, type="str"),
                                ),
                            ),
                            port_groups=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    count=dict(required=False, type="int"),
                                    roles=dict(required=False,
                                               type="list", elements="str"),
                                    speed=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=False, type="str"),
                                            value=dict(
                                                required=False, type="int"),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            port=dict(required=False, type="int"),
            server=dict(required=False, type="str"),
            servers=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    connectivity_type=dict(
                        required=True,
                        type="str",
                    ),
                    count=dict(
                        required=True,
                        type="int",
                    ),
                    label=dict(
                        required=True,
                        type="str",
                    ),
                    logical_device=dict(
                        required=True,
                        type="str",
                    ),
                    ip_version=dict(
                        required=True,
                        type="str",
                    ),
                    port_channel_id_min=dict(
                        required=True,
                        type="int",
                    ),
                    port_channel_id_max=dict(
                        required=True,
                        type="int",
                    ),
                    links=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            attachment_type=dict(required=False, type="str"),
                            label=dict(required=False, type="str"),
                            lag_mode=dict(required=False, type="str"),
                            leaf_peer=dict(required=False, type="str"),
                            link_per_switch_count=dict(
                                required=False, type="int"),
                            link_speed=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    unit=dict(required=False, type="str"),
                                    value=dict(required=False, type="int"),
                                ),
                            ),
                            target_switch_label=dict(
                                required=False, type="str"),
                        ),
                    ),
                ),
            ),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            tags=dict(
                required=False,
                type="list",
                elements="str",
            ),
            validate_certs=dict(type="bool", required=False, default=False),
        )

    @staticmethod
    def design_template_spec():
        """Defined the data model for creating a new design template."""
        return dict(
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_API_TOKEN", "APSTRA_API_TOKEN", "API_TOKEN"],
                ),
                no_log=True,
                type="str",
            ),
            description=dict(required=False, type="str"),
            dhcp_service_intent=dict(required=False, type="dict", options=dict(
                active=dict(required=False, type="str"))),
            display_name=dict(
                required=True,
                type="str",
            ),
            id=dict(required=False, type="str"),
            mesh_link_speed=dict(
                required=False,
                type="dict",
                options=dict(
                    unit=dict(required=False, type="str"),
                    value=dict(required=False, type="int"),
                ),
            ),
            mesh_link_count=dict(required=False, type="int"),
            port=dict(required=False, type="int"),
            rack_type_counts=dict(
                required=True,
                type="list",
                elements="dict",
                options=dict(
                    count=dict(
                        required=True,
                        type="int",
                    ),
                    rack_type_id=dict(
                        required=True,
                        type="str",
                    ),
                ),
            ),
            rack_types=dict(
                required=True,
                type="list",
                elements="dict",
                options=dict(
                    access_switches=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            access_access_link_count=dict(
                                required=True,
                                type="int",
                            ),
                            access_access_link_speed=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    unit=dict(
                                        required=True,
                                        type="str",
                                    ),
                                    value=dict(
                                        required=True,
                                        type="int",
                                    ),
                                ),
                            ),
                            instance_count=dict(
                                required=True,
                                type="int",
                            ),
                            label=dict(
                                required=True,
                                type="str",
                            ),
                            links=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    attachment_type=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    lag_mode=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    link_per_switch_count=dict(
                                        required=False, type="int"),
                                    link_speed=dict(
                                        required=False,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=True,
                                                type="str",
                                            ),
                                            value=dict(
                                                required=True,
                                                type="int",
                                            ),
                                        ),
                                    ),
                                    tags=dict(required=True, type="list",
                                              elements="str"),
                                    target_switch_label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                ),
                            ),
                            logical_device=dict(
                                required=True,
                                type="str",
                            ),
                            redundancy_protocol=dict(
                                required=True,
                                type="str",
                            ),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                        ),
                    ),
                    description=dict(required=False, type="str"),
                    display_name=dict(
                        required=False,
                        type="str",
                    ),
                    fabric_connectivity_design=dict(required=True, type="str"),
                    generic_systems=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            asn_domain=dict(
                                required=True,
                                type="str",
                            ),
                            count=dict(
                                required=True,
                                type="int",
                            ),
                            label=dict(
                                required=True,
                                type="str",
                            ),
                            links=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    attachment_type=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    lag_mode=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    link_per_switch_count=dict(
                                        required=False,
                                        type="int",
                                    ),
                                    link_speed=dict(
                                        required=False,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=True,
                                                type="str",
                                            ),
                                            value=dict(
                                                required=True,
                                                type="int",
                                            ),
                                        ),
                                    ),
                                    switch_peer=dict(
                                        required=False, type="str"),
                                    tags=dict(required=True, type="list",
                                              elements="str"),
                                    target_switch_label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                ),
                            ),
                            logical_device=dict(
                                required=True,
                                type="str",
                            ),
                            loopback=dict(
                                required=True,
                                type="str",
                            ),
                            management_level=dict(
                                required=True,
                                type="str",
                            ),
                            port_channel_id_max=dict(
                                required=True,
                                type="int",
                            ),
                            port_channel_id_min=dict(
                                required=True,
                                type="int",
                            ),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                        ),
                    ),
                    id=dict(required=False, type="str"),
                    leafs=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            label=dict(
                                required=False,
                                type="str",
                            ),
                            leaf_leaf_l3_link_count=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_l3_link_port_channel_id=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_l3_link_speed=dict(
                                required=False,
                                type="str",
                            ),
                            leaf_leaf_link_count=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_link_port_channel_id=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_link_speed=dict(
                                required=False,
                                type="str",
                            ),
                            link_per_spine_count=dict(
                                required=False,
                                type="int",
                            ),
                            logical_device=dict(
                                required=False,
                                type="str",
                            ),
                            redundancy_protocol=dict(
                                required=False,
                                type="str",
                            ),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                        ),
                    ),
                    logical_devices=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            display_name=dict(
                                required=True,
                                type="str",
                            ),
                            id=dict(
                                required=True,
                                type="str",
                            ),
                            panels=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    panel_layout=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            row_count=dict(
                                                required=False, type="int"),
                                            column_count=dict(
                                                required=False, type="int"),
                                        ),
                                    ),
                                    port_indexing=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            order=dict(
                                                required=False, type="str"),
                                            start_index=dict(
                                                required=False, type="int"),
                                            schema=dict(
                                                required=False, type="str"),
                                        ),
                                    ),
                                    port_groups=dict(
                                        required=False,
                                        type="list",
                                        elements="dict",
                                        options=dict(
                                            count=dict(
                                                required=False, type="int"),
                                            roles=dict(required=False,
                                                       type="list", elements="str"),
                                            speed=dict(
                                                required=True,
                                                type="dict",
                                                options=dict(
                                                    unit=dict(
                                                        required=False, type="str"),
                                                    value=dict(
                                                        required=False, type="int"),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                    servers=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            connectivity_type=dict(
                                required=True,
                                type="str",
                            ),
                            count=dict(
                                required=True,
                                type="int",
                            ),
                            label=dict(
                                required=True,
                                type="str",
                            ),
                            logical_device=dict(
                                required=True,
                                type="str",
                            ),
                            ip_version=dict(
                                required=True,
                                type="str",
                            ),
                            port_channel_id_min=dict(
                                required=True,
                                type="int",
                            ),
                            port_channel_id_max=dict(
                                required=True,
                                type="int",
                            ),
                            links=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    attachment_type=dict(
                                        required=False, type="str"),
                                    label=dict(required=False, type="str"),
                                    lag_mode=dict(required=False, type="str"),
                                    leaf_peer=dict(required=False, type="str"),
                                    link_per_switch_count=dict(
                                        required=False, type="int"),
                                    link_speed=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=False, type="str"),
                                            value=dict(
                                                required=False, type="int"),
                                        ),
                                    ),
                                    target_switch_label=dict(
                                        required=False, type="str"),
                                ),
                            ),
                        ),
                    ),
                    tags=dict(
                        required=False,
                        type="list",
                        elements="str",
                    ),
                ),
            ),
            type=dict(required=True, type="str"),
            virtual_network_policy=dict(
                required=True,
                type="dict",
                options=dict(
                    overlay_control_protocol=dict(required=True, type="str"),
                ),
            ),
            server=dict(required=False, type="str"),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            tags=dict(
                required=False,
                type="list",
                elements="str",
            ),
            validate_certs=dict(type="bool", required=False, default=False),
        )
