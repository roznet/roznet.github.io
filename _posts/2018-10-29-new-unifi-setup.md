---
layout: post
title:  "Upgrading my home network to Unifi"
date:   2018-10-28 09:57:13 +0100
categories: network
comments: true
---

I have been increasing the sophistication of my home network over the year. It all started when my network was not [intermittently not working]({{ site.baseurl }}{% post_url 2018-11-12-network-issues %}), internet connection regularly dropping for minutes at a time and driving my whole family nuts.

As I learned more and more about networking to fix the problem, I had build a complex setup using a NUC as a linux server, with an [openvpn server](https://openvpn.net/), network latency monitoring using [SmokePing](https://oss.oetiker.ch/smokeping/), IDS using [snort](https://www.snort.org/) and [snorby](https://github.com/Snorby/snorby), traffic monitoring using [ntopng](https://www.ntop.org/products/traffic-analysis/ntop/) and a few other security tools.

It was a nice setup with mostly netgear hardware. It was working ok, but I had read about Unifi for a while and decided to try to upgrade my setup using that setup. My goals were to

1. make sure roaming accross the house and 2G and 5G band would become smoother.
2. setup VLANs so I could isolate guests and IOT devices like cameras etc from my main network

## The environment

My house is quite vertical with 4 floors and narrow. Each level having one or two rooms. The wifi signal does not go well through the floors, and in my previous setup I have at least one access point per floor. This is a typical narrow semi-detached house in the UK, and therefore many neighbors wifi network are visible. I have ethernet cabling going to most room and I try to get the maximum devices hardwired.


## My setup

I went a bit overboard. I ordered the 5-packs Unifi Nano-HD and 4 Unifi 8 Port Switch so I would have one pair for each room.

For the main cabinet in the basement where all the cables converge I got a Unifi 24 port switch.

I chose the [USG 4 Pro](https://google.com/search?q=unifi+usg+4+pro) while using as [AAISP](https://aa.net.uk) which I highly recommend. The main reason being that my neighborhood is going to be a pilot for a new 330mbps services, and I wanted to be ready to handle the higher speed with the IDS feature turned on.

I installed the current latest version 5.9.29 of the [unifi controller](https://help.ubnt.com/hc/en-us/articles/220066768-UniFi-How-to-Install-Update-via-APT-on-Debian-or-Ubuntu) on a ubuntu 18.04 install on an [intel NUC](https://www.intel.com/content/www/us/en/products/boards-kits/nuc.html) computer.

All the basics worked pretty much out of the box. Though I had a few issues to revolve, which I'll write about in future posts.

1. [IPV6 setup]({{ site.baseurl }}{% post_url 2018-11-17-fixing-ipv6-unifi-gateway-aaisp %})
2. [ntopng setup]({{ site.baseurl }}{% post_url 2018-11-fixing-ntopng-for-unifi-gateway %})
3. [DNS server for local devices]({{ site.baseurl }}{% post_url 2018-12-08-ipv6-dns-local-hosts %})





