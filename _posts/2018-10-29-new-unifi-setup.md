---
layout: post
title:  "Upgrading my home network to Unifi"
date:   2018-10-28 09:57:13 +0100
categories: network
comments: true
---

I have been increasing the sophistication of my home network over the year. It all started when my network was not intermittently not working, internet connection regularly dropping for minutes at a time and driving my whole family nuts, but this is a story for another time and it's not fixed.

As I learned more and more about networking to fix the problem, I had build a complexed setup using a NUC as a linux server, with my own vpn server, network latency monitoring using SmokePing, IDS using snort and snorby, traffic monitoring using ntopng and a few other security tools.

It was old build with older netgear hardware, and was working ok, but I decided to try to upgrade my setup using a Unifi setup. While the setup was quite smooth, I had two issues to still sort out:

- ipv6 was not working out of the box. 
- my ntopng monitoring computer does not work anymore because the port mirroring does not work the same way as the old netgear hardware.

## My setup

I upgraded my setup to a [USG 4 Pro](https://google.com/search?q=unifi+usg+4+pro) while using as [AAISP](https://aa.net.uk) which I highlight recommend. Everything worked pretty much out of the box. I had installed the current latest version 5.9.29 of the [unifi controller](https://help.ubnt.com/hc/en-us/articles/220066768-UniFi-How-to-Install-Update-via-APT-on-Debian-or-Ubuntu) on a ubuntu 18.04 install on an [intel NUC](https://www.intel.com/content/www/us/en/products/boards-kits/nuc.html) computer.

Everything worked great out of the box and was very straight forward to setup. Except for the IPV6 setup...

