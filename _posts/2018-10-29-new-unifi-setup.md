---
layout: post
title:  "Upgrading my home network to Unifi"
date:   2018-10-28 09:57:13 +0100
categories: network
---

I have been increasing the sophistication of my home network over the year. It all started when my network was not intermittently not working, internet connection regularly dropping for minutes at a time and driving my whole family nuts, but this is a story for another time and it's not fixed.

As I learned more and more about networking to fix the problem, I had build a complexed setup using a NUC as a linux server, with my own vpn server, network latency monitoring using SmokePing, IDS using snort and snorby, traffic monitoring using ntopng and a few other security tools.

It was old build with older netgear hardware, and was working ok, but I decided to try to upgrade my setup using a Unifi setup. While the setup was quite smooth, I had two issues to still sort out:

- ipv6 was not working out of the box. I figured out how to fix after comparing the configuration of the edgerouter I have previously. I still need to make sure I build and test a proper config.gateway.json file to ensure the fix persits through reboot of the gateway.
- my ntopng monitoring computer does not work anymore because the port mirroring does not work the same way as the old netgear hardware. Still working on this one.




