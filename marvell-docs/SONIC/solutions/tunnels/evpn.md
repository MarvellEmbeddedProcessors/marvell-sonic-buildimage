# EVPN (VXLAN)

This guide shows how to configure and verify a Layer 2 **EVPN VXLAN** overlay
on Prestera SONiC with two switches (VTEPs) that stretch one VLAN between two
hosts. BGP L2VPN-EVPN is the control plane and VXLAN is the data plane.
Refer to the [EVPN SONiC HLD](https://github.com/sonic-net/SONiC/blob/master/doc/vxlan/EVPN/EVPN_VXLAN_HLD.md)
for more details.

## Prerequisites

- Two switches running Prestera SONiC (`switch1`, `switch2`) and two hosts
  (`host1`, `host2`), cabled as shown in the topology.
- An image with the `bgp` container (FRR) running. The EVPN control plane
  uses `vtysh` on each switch. Check on each switch:

  ```text
  switch1> docker ps | grep bgp
  ```

## Topology

```{image} images/2switch-evpn-topo.svg
:alt: EVPN VXLAN topology with two VTEPs and two hosts
:width: 100%
```

```{raw} html
<p style="text-align:center; text-decoration:underline; font-size:1.05em; font-weight:600;">Packet Transformation in EVPN</p>
```

```{image} images/evpn-packet-format.svg
:alt: Packet transformation: original frame, VXLAN packet, original frame
:width: 100%
:align: center
```

## Configurations

- **switch1: underlay, VLAN, VTEP and VNI mapping.** `Ethernet0` is the
  underlay link; `Ethernet1` is the untagged access port for `host1`. The
  VTEP source IP is the underlay address:

  ```text
  switch1> sudo config interface ip add Ethernet0 10.1.1.0/31
  switch1> sudo config interface startup Ethernet0
  switch1> sudo config vlan add 100
  switch1> sudo config vlan member add 100 Ethernet1 -u
  switch1> sudo config interface startup Ethernet1
  switch1> sudo config interface ip add Vlan100 192.168.100.1/24
  switch1> sudo config vxlan add vtep1 10.1.1.0
  switch1> sudo config vxlan evpn_nvo add nvo1 vtep1
  switch1> sudo config vxlan map add vtep1 100 1000
  ```

- **switch2: the mirror configuration** with its own addresses:

  ```text
  switch2> sudo config interface ip add Ethernet0 10.1.1.1/31
  switch2> sudo config interface startup Ethernet0
  switch2> sudo config vlan add 100
  switch2> sudo config vlan member add 100 Ethernet1 -u
  switch2> sudo config interface startup Ethernet1
  switch2> sudo config interface ip add Vlan100 192.168.100.2/24
  switch2> sudo config vxlan add vtep1 10.1.1.1
  switch2> sudo config vxlan evpn_nvo add nvo1 vtep1
  switch2> sudo config vxlan map add vtep1 100 1000
  ```

- **switch1: BGP EVPN.** Peer with `switch2` over the underlay, activate the
  `l2vpn evpn` address family, advertise all local VNIs, advertise the SVI IP and set the VNI route
  targets:

  ```text
  switch1> sudo vtysh \
      -c 'configure terminal' \
      -c 'router bgp 65001' \
      -c ' bgp router-id 10.1.1.0' \
      -c ' no bgp ebgp-requires-policy' \
      -c ' neighbor 10.1.1.1 remote-as 65002' \
      -c ' address-family l2vpn evpn' \
      -c '  neighbor 10.1.1.1 activate' \
      -c '  advertise-all-vni' \
      -c '  vni 1000' \
      -c '   route-target import 1:1000' \
      -c '   route-target export 1:1000' \
      -c '  exit-vni' \
      -c '  advertise-svi-ip' \
      -c ' exit-address-family'
  ```

- **switch2: BGP EVPN** with its own AS, router ID and peer:

  ```text
  switch2> sudo vtysh \
      -c 'configure terminal' \
      -c 'router bgp 65002' \
      -c ' bgp router-id 10.1.1.1' \
      -c ' no bgp ebgp-requires-policy' \
      -c ' neighbor 10.1.1.0 remote-as 65001' \
      -c ' address-family l2vpn evpn' \
      -c '  neighbor 10.1.1.0 activate' \
      -c '  advertise-all-vni' \
      -c '  vni 1000' \
      -c '   route-target import 1:1000' \
      -c '   route-target export 1:1000' \
      -c '  exit-vni' \
      -c '  advertise-svi-ip' \
      -c ' exit-address-family'
  ```

- **Hosts: put both NICs in the same subnet.** The address is on the NIC
  cabled to the switch:

  ```text
  host1> sudo ip link set eth1 up
  host1> sudo ip addr add 192.168.100.11/24 dev eth1
  ```

  ```text
  host2> sudo ip link set eth1 up
  host2> sudo ip addr add 192.168.100.12/24 dev eth1
  ```

## Verify

- **Underlay reachability.** `switch1` must reach the peer VTEP address:

  ```text
  switch1> ping -c 3 10.1.1.1
  PING 10.1.1.1 (10.1.1.1) 56(84) bytes of data.
  64 bytes from 10.1.1.1: icmp_seq=1 ttl=64 time=8.66 ms
  64 bytes from 10.1.1.1: icmp_seq=2 ttl=64 time=91.4 ms
  64 bytes from 10.1.1.1: icmp_seq=3 ttl=64 time=49.7 ms

  --- 10.1.1.1 ping statistics ---
  3 packets transmitted, 3 received, 0% packet loss, time 2003ms
  ```

- **BGP session.** Wait up to a couple of minutes after configuring. The
  first session after a cold boot can take longer than later ones. The state
  must be `Established`:

  ```text
  switch1> sudo vtysh -c 'show bgp neighbors 10.1.1.1' | grep -i 'BGP state'
  BGP state = Established, up for 00:01:47
  ```

- **EVPN routes.** Each switch has its own routes (next hop `10.1.1.0`, weight
  32768) and the peer's routes (next hop `10.1.1.1`, path `65002`). Type-2
  routes carry host MACs and type-3 routes carry the VTEP flood list:

  ```text
  switch1> sudo vtysh -c 'show bgp l2vpn evpn'
     Network          Next Hop            Metric LocPrf Weight Path
  Route Distinguisher: 10.1.1.0:2
   *>  [2]:[0]:[48]:[0c:f8:9a:01:00:01]
                      10.1.1.0                           32768 i
                      ET:8 RT:1:1000
   *>  [3]:[0]:[32]:[10.1.1.0]
                      10.1.1.0                           32768 i
                      ET:8 RT:1:1000
  Route Distinguisher: 10.1.1.1:2
   *>  [2]:[0]:[48]:[0c:9f:af:c2:00:01]
                      10.1.1.1                               0 65002 i
                      RT:1:1000 ET:8
   *>  [3]:[0]:[32]:[10.1.1.1]
                      10.1.1.1                               0 65002 i
                      RT:1:1000 ET:8

  Displayed 4 out of 4 total prefixes
  ```

- **VNI and remote VTEP in FRR.** VNI 1000 is a Layer 2 VNI on VLAN 100 with
  one remote VTEP:

  ```text
  switch1> sudo vtysh -c 'show evpn vni'
  VNI        Type VxLAN IF              # MACs   # ARPs   # Remote VTEPs  Tenant VRF
  1000       L2   vtep1-100             2        0        1               default

  switch1> sudo vtysh -c 'show evpn vni 1000'
  VNI: 1000
   Type: L2
   Vlan: 100
   Bridge: Bridge
   Tenant VRF: default
   VxLAN interface: vtep1-100
   SVI interface: Vlan100
   Local VTEP IP: 10.1.1.0
   Remote VTEPs for this VNI:
    10.1.1.1 flood: HER
   Number of MACs (local and remote) known for this VNI: 2
  ```

- **VXLAN configuration and remote VTEP.** The tunnel, the VLAN to VNI map,
  and the remote VTEP learned through EVPN (*Creation Source* `EVPN`):

  ```text
  switch1> show vxlan tunnel
  vxlan tunnel name    source ip    destination ip    tunnel map name    tunnel map mapping(vni -> vlan)
  -------------------  -----------  ----------------  -----------------  ---------------------------------
  vtep1                10.1.1.0                       map_1000_Vlan100   1000 -> Vlan100

  switch1> show vxlan interface
  VTEP Information:

          VTEP Name : vtep1, SIP  : 10.1.1.0
          NVO Name  : nvo1,  VTEP : vtep1
          Source interface  : Not Configured

  switch1> show vxlan remotevtep
  +----------+----------+-------------------+--------------+
  | SIP      | DIP      | Creation Source   | OperStatus   |
  +==========+==========+===================+==============+
  | 10.1.1.0 | 10.1.1.1 | EVPN              | oper_up      |
  +----------+----------+-------------------+--------------+
  Total count : 1
  ```

- **Data plane.** Ping across the tunnel from `host1` to `host2`. The result
  must show `0% packet loss`:

  ```text
  host1> ping -c 5 -I eth1 192.168.100.12
  PING 192.168.100.12 (192.168.100.12) from 192.168.100.11 eth1: 56(84) bytes of data.
  64 bytes from 192.168.100.12: icmp_seq=1 ttl=64 time=234 ms
  64 bytes from 192.168.100.12: icmp_seq=2 ttl=64 time=11.9 ms
  64 bytes from 192.168.100.12: icmp_seq=3 ttl=64 time=95.4 ms
  64 bytes from 192.168.100.12: icmp_seq=4 ttl=64 time=50.0 ms
  64 bytes from 192.168.100.12: icmp_seq=5 ttl=64 time=46.7 ms

  --- 192.168.100.12 ping statistics ---
  5 packets transmitted, 5 received, 0% packet loss, time 4006ms
  ```

- **MAC table.** After the ping, `switch1` shows `host1` locally on
  `Ethernet1` and `host2` as a static entry against the remote VTEP IP:

  ```text
  switch1> show mac
  No.    Vlan  MacAddress         Port       Type
  -----  ------  -----------------  ---------  -------
      1     100  0C:F8:9A:01:00:01  Ethernet1  Dynamic
      2     100  0C:9F:AF:C2:00:01  10.1.1.1   Static
  Total number of entries 2
  ```

- **Port counters.** Traffic crossed the access port (`Ethernet1`) and the
  underlay port (`Ethernet0`); errors and drops stay at 0:

  ```text
  switch1> show interfaces counters
      IFACE    STATE    RX_OK    RX_BPS    RX_UTIL    RX_ERR    RX_DRP    RX_OVR    TX_OK    TX_BPS    TX_UTIL    TX_ERR    TX_DRP    TX_OVR
  ----------  -------  -------  --------  ---------  --------  --------  --------  -------  --------  ---------  --------  --------  --------
   Ethernet0        U       49       N/A        N/A         0         0         0       49       N/A        N/A         0         0         0
   Ethernet1        U       17       N/A        N/A         0         0         0       56       N/A        N/A         0         0         0
  ```

## Clean up

```text
switch1> sudo vtysh -c 'configure terminal' -c 'no router bgp 65001'
switch1> sudo config vxlan map del vtep1 100 1000
switch1> sudo config vxlan evpn_nvo del nvo1
switch1> sudo config vxlan del vtep1
switch1> sudo config interface ip remove Vlan100 192.168.100.1/24
switch1> sudo config vlan member del 100 Ethernet1
switch1> sudo config vlan del 100
switch1> sudo config interface ip remove Ethernet0 10.1.1.0/31
```
