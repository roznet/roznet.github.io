---
layout: post
title: "Setting up ntopng with Unifi USG Gateway"
date: 2018-11-29 11:38:00 +0100
---

After [upgrading my home network]({{ site.baseurl }}{% post_url 2018-10-29-new-unifi-setup %}) to a Unifi system, I could use the Unifi Controller to see activity on the network, but the current version only display activity level with very few details by hosts. I gotten used to [ntopng](https://www.ntop.org/products/traffic-analysis/ntop/) and its details both of what is happening at a given moment and ability to look back historically. Very useful for troubleshooting or investigating unexpected behavior. The Unifi Controller while providing great high level insight, still fell short of this ability, so I decided to re-enable by ntopng setup.

## Device setup

I setup ntopng on a [NUC device](https://www.intel.com/content/www/us/en/products/boards-kits/nuc.html) where I installed [ubuntu 18.04](https://www.ubuntu.com/). Ubuntu comes with ntopng as a standard packages in their apt repo, so I just used that to install with `sudo apt-get install ntopng`. Easy enough.

The NUC is connected via its ethernet port to the main Unifi Switch, the idea was to setup this port as a mirror to the port going from the Unifi Switch ot the  Gateway, so that all the traffic to the internet is mirrored and monitored.

## Mirroring port

The first problem I encountered was to get my instance of ntopng to work with the unifi switch. 

In my previous setup, I was using a netgear prosafe gs116Ev2. I had not realised that the setup of the mirroring of a port in the prosafe was somewhat unusual in that it was also allowing traffic up and behaving like a regular port. On the unifi switch, the the mirror port only receive the traffic from the port being monitored, so the interface connected to that port becomes unusable to access the network. 

Whenever I turned on the mirroring on the port connected to the ethernet interface of the NUC, the computer would loose all connectivity to the network. The NUC computer has both wifi and ethernet. So I tried to sort out how to use the wifi interface for commication on the network while the ethernet would be receiving the mirrored traffic.

## Configuration of a second interface

I first tried to configure the network routes to prefer the wifi interface to access the network using `metric` in the `/etc/network/interfaces` file. But somehow the route would always add a prioritised route via the ethernet port:

{% highlight bash %}
user@host: route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    600    0        0 wlp58s0
0.0.0.0         192.168.1.1     0.0.0.0         UG    700    0        0 eno1
169.254.0.0     0.0.0.0         255.255.0.0     U     1000   0        0 eno1
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eno1
192.168.1.0     0.0.0.0         255.255.255.0   U     600    0        0 wlp58s0
{% endhighlight %}

I [never figured out](https://askubuntu.com/questions/1088396/how-to-use-wifi-for-lan-and-internet-access-and-ethernet-for-traffic-monitoring) how to avoid that. But went a different route: I got a usb ethernet device, and added a new interface, so I would not have to figure out how to prioritize the wifi interface and would probably be more efficient.

After adding the usb interface it was still prioritizing the ethernet port. So I decided to test if the order in the `/etc/interfaces` file may help configure the priority of the interface.

But first the USB Interface came back with a really long name which contained the full MAC address in the name... Which made it unsatisfying and complicated to add to the file. This got resolved by adding a `/etc/udev/rules.d/70-persistent-net.rules` files as such:

{% highlight bash %}
# usb interface
#

SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="00:XX:XX:XX:XX:XX", ATTR{dev_id}=="0x0", ATTR{type}=="1", NAME="enus
b1"
{% endhighlight %}

After I entered explicitely in the `/etc/network/interfaces` file both interface name in the desired order, all started to works as expected. Both interface have a zero metrics, but the order is fine, the enusb1 interface receives all the mirrored traffic, eno1 is the interface used to access the network 

{% highlight bash %}
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    0      0        0 eno1
0.0.0.0         192.168.1.1     0.0.0.0         UG    600    0        0 wlp58s0
169.254.0.0     0.0.0.0         255.255.0.0     U     1000   0        0 eno1
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eno1
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 enusb1
192.168.1.0     0.0.0.0         255.255.255.0   U     600    0        0 wlp58s0
{% endhighlight %}

and ntopng reported the traffic fine!









