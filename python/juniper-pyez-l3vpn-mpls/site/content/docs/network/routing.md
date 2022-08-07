This section explains our generated MPLS configurations.

## Routing

To best emulate a small ISP, I have opted to use OSPF between the MPLS routers, with external BGP peering with both customer connections.

> **PE1 Configuration: OSPF to MPLS backbone**

```
set protocols ospf area 0.0.0.0 interface ge-0/0/2.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface ge-0/0/3.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface lo0.0 passive
```

> **PE1 Configuration: external BGP to CE1**

```
set routing-instances Customer1 instance-type vrf
set routing-instances Customer1 protocols bgp group Customer1 type external
set routing-instances Customer1 protocols bgp group Customer1 peer-as 65000
set routing-instances Customer1 protocols bgp group Customer1 neighbor 74.51.192.1
```

As iBGP is needed to signal PE routers to share L3VPN routes, we will of course be using it for that usecase in our topology.

> **PE1 Configuration: L3VPN PE4**

```
set protocols bgp group MPLS type internal
set protocols bgp group MPLS local-address 192.168.255.11
set protocols bgp group MPLS family inet-vpn unicast
set protocols bgp group MPLS peer-as 300
set protocols bgp group MPLS neighbor 192.168.255.16

```
