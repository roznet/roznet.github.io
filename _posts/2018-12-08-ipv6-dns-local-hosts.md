---
layout: post
title:  "Accessing hosts on local network by name via DNS with IPV6 and Unifi USG Gateway"
date:   2018-12-08 09:57:13 +0100
categories: network
comments: true
---

One of the challenges of my network setup was to ensure that I could access the different services I am running on different services via hostname. For that I needed to make sure that the DNS forwarded on my Unifi USG Gateway was properly setup and with the list of host names. These involved several steps to get everything right

## Getting the list of hosts and IP in the Unifi Gateway

The first thing was to get the list of hostname and ip to be known by the Unifi Gateway. This is currently not possible from the Unifi Controller interface. I used the `system/static-host-mapping/host-name` settings, by editing the config.gateway.json file on the unifi controller site config, with entries as below:

```json
{
  "imac.localnet" : {
    "inet" : "192.168.11.117"
  },
  "wifibasement.localnet" : {
    "inet" : "192.168.11.34"
  },
  "printer.localnet" : {
    "inet" : "192.168.11.126"
  },
  "switchbasement.localnet" : {
    "inet" : "192.168.11.104"
  },
}
```

Because I have historically maintained the list of my network devices with [a python script](https://github.com/roznet/quickutils), I also updated it with the ability to generate the list automatically as below. This is quite convenient as much easier to keep in sync and load many hosts at once - I have about 20 devices with a hostname.

```bash
user:imac$ ./lancheck.py show -dstatic_host_mapping
{
  "system": {
    "static-host-mapping": {
      "host-name": {
        "imac.localnet": {
          "inet": "192.168.11.117"
        }, 
        "wifibasement.localnet": {
          "inet": "192.168.11.34"
        }, 

```

Of course, an important step is to make sure the relevant host have a fix IP. To achieve that, I mixed two methods: 

1. on some device I configured the system to not use dhcp but a static IP within the reservation I defined in the router config (from the unifi controller, in the network config page:
![Network Config](/assets/networkconfig.png)

2. Configuring a fixed IP from the unifi controller user interface, in the network pane of the config pane, as below:

<img src="/assets/devicestatic.png" width="320px"  />

After reprovision, you can then verify that the Unifi Gateway pick up the hostname by using nslookup:

```bash

user:imac$ nslookup imac.localnet router.localnet
Server:		router.localnet
Address:	192.168.1.1#53

Name:	imac.localnet
Address: 192.168.1.117
```

## Ensuring that all device use the Unifi Gateway as DNS name server

While everything was working in ipv4, one issue that continued bugging me for a while was that on iPhone or other devices running on ipv6, I was unable to access devices on my local network by their host names, it was resulting in host not found. The DNS Setting of these device would show that beside the ipv4 address of the gateway, it also had the ipv6 address of the dns server of my ISP. And somehow the devices would not revert to the ipv4 dns server in my Unifi Gateway, but just fail to resolve the hostname.

This took me a while to figure out. I thought changing the behavior of the phone would likely be impossible, so I had to understand how the DNS of the ISP was making it to the device and how to prevent that.

First I researched if it would be possible to setup DHCPv6 or assign the IPV6 address to some fixed value, but that felt way to complicated and the SLAAC process that was used by my network resulted in randomly and temporarily set addresses.

The DNS of the ISP was being acquired during the SLAAC process I believe, so I tried to find out if I could prevent that from happening so that only the gateway would be use.

I found out that there was a setting that I could set in the config of the gateway to not transmit the dns setting to the interface of the lan, as below by connecting to the Unifi Gateway via SSH:

```bash
configure
set interfaces ethernet eth2 pppoe 0 dhcpv6-pd pd 0 interface eth0 no-dns
commit
save
```

This resulted in the device only getting the Unifi Gateway as a dns server and no longer the ISP dns server. The local host are now found by name on all my devices...

The one missing piece is that I could not figure out how to set that no-dns setting on the config.gateway.json, trying to extract the config by using `mca-` showed not value related to no-dns in the file, while it's clearly there on the `configure` output as show below.

So it works, but on reboot of the unifi gateway, it is necessary to re-issue the configure command at the moment...

<img src="/assets/nodnsconfigure.png" width="50%"/>
<img src="/assets/nodnsjson.png" width="50%"/>







