# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import env_fallback


class Response(object):
    """Custom HTTP response object."""

    def __init__(self, resp, info):
        self.body = None
        if resp:
            self.body = resp.read()
        self.info = info

    @property
    def json(self):
        """Return JSON body from response."""
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


class MistHelper:
    """Define HTTP methods and data model specs used by the Ansible modules."""

    def __init__(self, module):
        """Define attributes of our class."""
        self.module = module
        self.baseurl = module.params.get("baseurl", "https://api.mist.com/api/v1")
        self.timeout = module.params.get("timeout", 30)
        self.api_token = module.params.get("api_token")
        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-type": "application/json",
        }

        """Validate the api_token object against the API."""
        response = self.get("self")
        if response.status_code == 401:
            self.module.fail_json(msg="Failed to login using API token, please verify validity of API token.")

    def _url_builder(self, path):
        """Strip off leading / in the path."""
        if path[0] == "/":
            path = path[1:]
        return f"{self.baseurl}/{path}"

    def send(self, method, path, data=None):
        """Define REST API call."""
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
        """HTTP GET request."""
        return self.send("GET", path, data)

    def put(self, path, data=None):
        """HTTP PUT request."""
        return self.send("PUT", path, data)

    def post(self, path, data=None):
        """HTTP POST request."""
        return self.send("POST", path, data)

    def delete(self, path, data=None):
        """HTTP DELETE request."""
        return self.send("DELETE", path, data)

    @staticmethod
    def gateway_spec():
        """Data model for Wireless within Mist."""
        return dict(
            additional_config_cmds=dict(required=False, type="list", elements="str"),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ["MIST_API_KEY", "MIST_API_TOKEN"]),
                no_log=True,
                type="str",
            ),
            baseurl=dict(
                required=False,
                default="https://api.mist.com/api/v1",
                fallback=(env_fallback, ["MIST_BASE_URL"]),
                type="str",
            ),
            bgp_config=dict(
                required=False,
                type="list",
                options=dict(
                    name=dict(required=True, type="str"),
                    type=dict(required=True, type="str"),
                    local_as=dict(required=True, type="int"),
                    auth_key=dict(required=True, type="str"),
                    neighbors=dict(
                        required=True,
                        type="dict",
                        options=dict(
                            peer_ip=dict(required=True, type="str"),
                            neighbor_as=dict(required=False, type="int"),
                            export_policy=dict(required=False, type="str"),
                            import_policy=dict(required=False, type="str"),
                        ),
                    ),
                    export_policy=dict(required=False, type="str"),
                ),
            ),
            disable_auto_config=dict(required=False, default=False, type="bool"),
            gateway_mgmt=dict(
                required=False,
                type="dict",
                options=dict(
                    app_usage=dict(required=False, type="bool"),
                ),
            ),
            gatewaytemplate_id=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            notes=dict(required=False, type="str"),
            org_id=dict(required=True, fallback=(env_fallback, ["MIST_ORG_ID"]), type="str"),
            routing_policies=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    name=dict(required=False, type="str"),
                    terms=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            prefix=dict(required=False, type="str"),
                            network=dict(required=False, type="str"),
                            as_path=dict(required=False, type="int"),
                            protocol=dict(required=False, type="str"),
                            then=dict(required=False, type="str"),
                        ),
                    ),
                    secret=dict(required=False, type="str"),
                ),
            ),
            service_policies=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    tenants=dict(required=False, type="list", elements="str"),
                    services=dict(required=False, type="list", elements="str"),
                    action=dict(required=False, type="str"),
                    name=dict(required=False, type="str"),
                    path_preference=dict(required=False, type="str"),
                ),
            ),
            site_name=dict(required=False, type="str"),
            site_id=dict(required=False, type="str"),
            state=dict(required=True, choices=["present", "absent"], type="str"),
        )

    @staticmethod
    def site_spec():
        """Data model for the Site object within Mist."""
        return dict(
            address=dict(required=False, type="str"),
            alarmtemplate_id=dict(required=False, type="str"),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ["MIST_API_KEY", "MIST_API_TOKEN"]),
                no_log=True,
                type="str",
            ),
            baseurl=dict(
                required=False,
                default="https://api.mist.com/api/v1",
                fallback=(env_fallback, ["MIST_BASE_URL"]),
                type="str",
            ),
            country_code=dict(required=False, type="str"),
            gatewaytemplate_id=dict(required=True, type="str"),
            latlng=dict(
                required=False,
                type="dict",
                options=dict(
                    lat=dict(required=False, type="float"),
                    lng=dict(required=False, type="float"),
                ),
            ),
            name=dict(required=False, type="str"),
            notes=dict(required=False, type="str"),
            org_id=dict(required=True, fallback=(env_fallback, ["MIST_ORG_ID"]), type="str"),
            rftemplate_id=dict(required=False, type="str"),
            secpolicy_id=dict(required=False, type="str"),
            sitegroups=dict(required=False, type="list", elements="str"),
            state=dict(required=True, choices=["present", "absent"], type="str"),
            timeout=dict(required=False, type="int"),
            timezone=dict(required=False, type="str"),
            validate_certs=dict(type="bool", required=False),
            # vars=dict(
            #     required=False,
            #     type="list",
            #     elements="dict",
            #     options=dict(
            #         name=dict(required=False, type="str"),
            #         value=dict(required=False, type="str"),
            #     ),
            # ),
        )

    @staticmethod
    def site_groups_spec():
        """Data model for Site Groups object within Mist."""
        return dict(
            api_token=dict(
                required=True,
                fallback=(env_fallback, ["MIST_API_KEY", "MIST_API_TOKEN"]),
                no_log=True,
                type="str",
            ),
            baseurl=dict(
                required=False,
                default="https://api.mist.com/api/v1",
                fallback=(env_fallback, ["MIST_BASE_URL"]),
                type="str",
            ),
            name=dict(required=True, type="str"),
            org_id=dict(required=True, fallback=(env_fallback, ["MIST_ORG_ID"]), type="str"),
            site_ids=dict(required=False, type="list", elements="str"),
            state=dict(required=True, type="str"),
        )

    @staticmethod
    def wired_spec():
        """Data model for Wired switching within Mist."""
        return dict(
            additional_config_cmds=dict(required=False, type="list", elements="str"),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ["MIST_API_KEY", "MIST_API_TOKEN"]),
                no_log=True,
                type="str",
            ),
            baseurl=dict(
                required=False,
                default="https://api.mist.com/api/v1",
                fallback=(env_fallback, ["MIST_BASE_URL"]),
                type="str",
            ),
            disable_auto_config=dict(required=False, type="bool"),
            id=dict(required=False, type="str"),
            ip_config=dict(
                required=False,
                type="dict",
                options=dict(
                    type=dict(required=False, type="str"),
                    network=dict(required=False, type="str"),
                ),
            ),
            mac=dict(required=False, type="str"),
            model=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            networks=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    name=dict(required=False, type="str"),
                    vlan_id=dict(required=False, type="str"),
                ),
            ),
            notes=dict(required=False, type="str"),
            oob_ip_config=dict(
                required=False,
                type="dict",
                options=dict(
                    type=dict(required=False, type="str"),
                    network=dict(required=False, type="str"),
                ),
            ),
            org_id=dict(required=True, fallback=(env_fallback, ["MIST_ORG_ID"]), type="str"),
            port_config=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    name=dict(required=False, type="str"),
                    profile=dict(required=False, type="str"),
                ),
            ),
            port_profiles=dict(
                required=False,
                default=[],
                type="list",
                elements="dict",
                options=dict(
                    name=dict(required=True, type="str"),
                    all_networks=dict(required=False, type="bool"),
                    disabled=dict(required=False, type="bool"),
                    duplex=dict(required=False, type="str"),
                    mac_limit=dict(required=False, type="int"),
                    mode=dict(required=False, type="str"),
                    networks=dict(required=False, type="list"),
                    poe_disabled=dict(required=False, type="bool"),
                    port_auth=dict(required=False, type="str"),
                    port_network=dict(required=False, type="str"),
                    speed=dict(required=False, type="str"),
                    stp_edge=dict(required=False, type="bool"),
                    voip_network=dict(required=False, type="str"),
                ),
            ),
            port_usages=dict(
                required=False,
                type="dict",
                options=dict(
                    name=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            vlan_id=dict(required=False, type="str"),
                        ),
                    ),
                ),
            ),
            role=dict(required=False, type="str"),
            serial=dict(required=False, type="str"),
            site_id=dict(required=False, type="str"),
            site_name=dict(required=False, type="str"),
        )

    @staticmethod
    def wlan_spec():
        """Data model for Wireless within Mist."""
        return dict(
            airwatch=dict(
                required=False,
                type="dict",
                options=dict(
                    enabled=dict(required=False, type="bool"),
                    console_url=dict(required=False, type="str"),
                    api_key=dict(required=False, type="str"),
                    username=dict(required=False, type="str"),
                    password=dict(required=False, type="str"),
                ),
            ),
            allow_mdns=dict(required=False, default=False, type="bool"),
            allow_ipv6_ndp=dict(required=False, type="bool"),
            ap_ids=dict(required=False, type="list", elements="str"),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ["MIST_API_KEY", "MIST_API_TOKEN"]),
                no_log=True,
                type="str",
            ),
            apply_to=dict(required=False, type="str"),
            arp_filter=dict(required=False, type="bool"),
            auth=dict(
                required=False,
                type="dict",
                options=dict(
                    type=dict(
                        required=False,
                        choices=[
                            "open",
                            "psk",
                            "wep",
                            "eap",
                            "psk-tkip",
                            "psk-wpa2-tkip",
                        ],
                        type="str",
                    ),
                    psk=dict(required=False, type="str"),
                    enable_mac_auth=dict(required=False, type="bool"),
                    multi_psk_only=dict(required=False, type="bool"),
                    pairwise=dict(required=False, type="list", elements="str"),
                    wep_as_secondary_auth=dict(required=False, type="bool"),
                    private_wlan=dict(required=False, type="bool"),
                    keys=dict(required=False, type="list", elements="str"),
                    key_idx=dict(required=False, type="int"),
                    eap_reauth=dict(required=False, type="bool"),
                ),
            ),
            auth_servers_nas_id=dict(required=False, type="str"),
            auth_servers_nas_ip=dict(required=False, type="str"),
            auth_servers_timeout=dict(required=False, type="int"),
            auth_servers_retries=dict(required=False, type="int"),
            auth_server_selection=dict(required=False, type="str"),
            auth_servers=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    host=dict(required=False, type="str"),
                    port=dict(required=False, type="int"),
                    secret=dict(required=False, type="str"),
                ),
            ),
            acct_servers=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    host=dict(required=False, type="str"),
                    port=dict(required=False, type="int"),
                    secret=dict(required=False, type="str"),
                ),
            ),
            acct_interim_interval=dict(required=False, type="int"),
            band=dict(required=False, type="str"),
            band_steer=dict(required=False, type="bool"),
            band_steer_force_band5=dict(required=False, type="bool"),
            baseurl=dict(
                required=False,
                default="https://api.mist.com/api/v1",
                fallback=(env_fallback, ["MIST_BASE_URL"]),
                type="str",
            ),
            block_blacklist_clients=dict(required=False, type="bool"),
            cisco_cwa=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    enabled=dict(required=False, type="bool"),
                    allowed_subnets=dict(required=False, type="list", elements="str"),
                    allowed_hostnames=dict(required=False, type="list", elements="str"),
                ),
            ),
            client_limit_down_enabled=dict(required=False, type="bool"),
            client_limit_down=dict(required=False, type="int"),
            client_limit_up_enabled=dict(required=False, type="bool"),
            client_limit_up=dict(required=False, type="int"),
            coa_servers=dict(
                required=False,
                type="list",
                elements="dict",
                options=dict(
                    enabled=dict(required=False, type="bool"),
                    ip=dict(required=False, type="str"),
                    port=dict(required=False, type="int"),
                    secret=dict(required=False, type="str"),
                    disable_event_timestamp_check=dict(required=False, type="bool"),
                ),
            ),
            disable_11ax=dict(required=False, type="bool"),
            disable_uapsd=dict(required=False, type="bool"),
            disable_wmm=dict(required=False, type="bool"),
            dtim=dict(required=False, type="int"),
            dynamic_psk=dict(required=False, type="bool"),
            dynamic_vlan=dict(
                required=False,
                type="dict",
                options=dict(
                    enabled=dict(required=False, type="bool"),
                    type=dict(required=False, type="str"),
                    vlans=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            vlan=dict(required=False, type="str"),
                            name=dict(required=False, type="str"),
                        ),
                    ),
                    default_vlan_id=dict(required=False, type="int"),
                    local_vlan_ids=dict(required=False, type="list", elements="str"),
                ),
            ),
            enable_wireless_bridging=dict(required=False, type="bool"),
            enabled=dict(required=False, type="bool"),
            hide_ssid=dict(required=False, type="bool"),
            hostname_ie=dict(required=False, type="bool"),
            interface=dict(required=False, type="str"),
            isolation=dict(required=False, type="bool"),
            legacy_overds=dict(required=False, type="bool"),
            limit_bcast=dict(required=False, type="bool"),
            limit_probe_response=dict(required=False, type="bool"),
            max_idletime=dict(required=False, type="int"),
            mxtunnel_id=dict(required=False, type="str"),
            no_static_ip=dict(required=False, type="bool"),
            no_static_dns=dict(required=False, type="bool"),
            org_id=dict(required=True, fallback=(env_fallback, ["MIST_ORG_ID"]), type="str"),
            radsec=dict(
                required=False,
                type="dict",
                options=dict(
                    enabled=dict(required=False, type="bool"),
                    server_name=dict(required=False, type="str"),
                    servers=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            host=dict(required=False, type="str"),
                            port=dict(required=False, type="int"),
                        ),
                    ),
                    default_vlan_id=dict(required=False, type="int"),
                    local_vlan_ids=dict(required=False, type="list", elements="str"),
                ),
            ),
            rateset=dict(
                required=False,
                type="dict",
                options=dict(
                    # got to find a way to use the k/v used by mist api.
                    #   can't believe it, but they're using integers as keys
                    #   this won't work right away
                    twentyfour=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            min_rssi=dict(required=False, type="int"),
                            template=dict(required=False, type="str"),
                            legacy=dict(required=False, type="list", elements="str"),
                            ht=dict(required=False, type="str"),
                        ),
                    ),
                    five=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            min_rssi=dict(required=False, type="int"),
                            template=dict(required=False, type="str"),
                            legacy=dict(required=False, type="list", elements="str"),
                            ht=dict(required=False, type="str"),
                            vht=dict(required=False, type="str"),
                        ),
                    ),
                    default_vlan_id=dict(required=False, type="int"),
                    local_vlan_ids=dict(required=False, type="list", elements="str"),
                ),
            ),
            roam_mode=dict(required=False, type="str"),
            schedule=dict(
                required=False,
                type="dict",
                options=dict(
                    enabled=dict(required=False, type="bool"),
                    hours=dict(
                        required=False,
                        type="dict",
                        options=dict(
                            sun=dict(required=False, type="str"),
                            mon=dict(required=False, type="str"),
                            tue=dict(required=False, type="str"),
                            wed=dict(required=False, type="str"),
                            thr=dict(required=False, type="str"),
                            fri=dict(required=False, type="str"),
                            sat=dict(required=False, type="str"),
                        ),
                    ),
                ),
            ),
            sle_excluded=dict(required=False, type="bool"),
            site_name=dict(required=False, type="str"),
            site_id=dict(required=False, type="str"),
            ssid=dict(required=False, type="str"),
            state=dict(required=False, choices=["absent", "present"], type="str"),
            template_id=dict(required=False, type="str"),
            template_name=dict(required=False, type="str"),
            type=dict(required=False, choices=["template", "site"], type="str"),
            use_eapol_v1=dict(required=False, type="bool"),
            vlan_enabled=dict(required=False, type="bool"),
            vlan_id=dict(required=False, type="int"),
            vlan_pooling=dict(required=False, type="bool"),
            vlan_ids=dict(required=False, type="list", elements="str"),
            wlan_limit_up_enabled=dict(required=False, type="bool"),
            wlan_limit_up=dict(required=False, type="int"),
            wlan_limit_down_enabled=dict(required=False, type="bool"),
            wlan_limit_down=dict(required=False, type="int"),
            wxtunnel_id=dict(required=False, type="str"),
            wxtunnel_remote_id=dict(required=False, type="str"),
            wxtag_ids=dict(required=False, type="list", elements="str"),
        )
