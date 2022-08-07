# standard library
import json

# third party
import requests
from pydantic import BaseModel


# -----------------------------------------------------------------------------
# Structured payload stored as object type `WebhookData`
# -----------------------------------------------------------------------------
class MistApi(BaseModel):

    base_url: str
    site: str
    device: str
    token: str
    interface: str

    def shutdown_iface(self):
        """Tell Mist to disable my switch's interface."""

        url = f"{self.base_url}/sites/{self.site}/devices/{self.device}"
        payload = json.dumps(
            {
                "port_config": {
                    "ge-0/0/0": {"usage": "disabled", "description": ""},
                    "ge-0/0/1": {"usage": "vlan1099", "description": ""},
                    f"{self.interface}": {"usage": "disabled", "description": ""},
                    "xe-0/2/3, xe-0/2/0": {
                        "usage": "evpn_uplink",
                        "dynamic_usage": None,
                        "description": "",
                        "no_local_overwrite": False,
                    },
                },
            }
        )
        headers = {
            "authorization": f"Token {self.token}",
            "accept": "application/json",
            "content-type": "application/json",
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        return response.json()
