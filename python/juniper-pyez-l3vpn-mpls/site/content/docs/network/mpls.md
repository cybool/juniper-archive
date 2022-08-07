This section explains our generated MPLS configuration.

## MPLS

The MPLS-aware routers are tagged with the green label of "MPLS" in the vLabs topology. We will be using LDP for signaling labels, which will limit the features we can perform within the network while conversely making it easier to provision.

To build an MPLS neighborship with LDP between two router interfaces, you will see in the configurations that a few parameters need to be setup:

> **enable the family of MPLS on the interface configuration**

```
set interfaces ge-0/0/1.0 family mpls
```

> **list the interface under the protocols/mpls configuration**

```
set protocols mpls interface ge-0/0/1.0
set protocols ldp interface ge-0/0/1.0
```

#### L3VPN

Each router participating within the MPLS L3VPN circuit will build their route-distinguisher off a similar pattern to our loopbacks, `192.168.255.{x}:100`, where `{x}` represents the router's ID

```
set routing-instances Customer1 instance-type vrf
set routing-instances Customer1 route-distinguisher 192.168.255.11:100
```

The routes that we import and export will be managed by the `target:{a}:{b}` structure, where `{a}` represents the BGP ASN and `{b}` respresents the customer's ID

```
set routing-instances Customer1 vrf-target target:300:100
```
