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

Because I have historically maintained the list of my network device with [a python script](https://github.com/roznet/quickutils), I also updated it with the ability to generate the list automatically as below:

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


## Synchronizing the list of hosts



## Ensuring that all device use the Unifi Gateway as DNS name server

One issue that has been bugging me for a while was that on iPhone or other devices I was unable to access devices on my local network by their host names.



