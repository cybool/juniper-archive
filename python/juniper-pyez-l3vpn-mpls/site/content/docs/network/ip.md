This section explains our default IPv4 address schema

## IP Addressing

I take a pragmatic approach to building an IP address schema.

Each router will be given an ID of 11-17, and its loopback/router-id will be built upon it within the prefix of `192.168.255.{x}/32`, where `{x}` represents the local device's ID.

Additionally, P2P connections will follow a pattern of `10.{x}.{y}.{x}/24`, where `{x}` represents the local device's ID and `{y}` represents the ID of the remote router.

> **Example: Router1**

```yaml
loopback0 = "192.168.255.11"
router id = "192.168.255.11"
p2p to router2 = "10.11.12.11/24"
p2p to router3 = "10.11.13.11/24"
p2p to router5 = "10.11.15.11/24"
```
