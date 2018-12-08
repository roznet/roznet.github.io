---
layout: post
title: "Fixing ntopng for Unifi USG Gateway"
date: 2018-11-29 11:38:00 +0100
---

## Fixing ntopng

The next problem I encountered was to get my instance of ntopng to work with the unifi switch. Before I was using a netgear prosafe gs116Ev2. I had not realised that the setup of the mirroring of a port in the prosafe was somewhat unusual in that it was also allowing traffic up and behaving like a regular port. On the unifi switch, the the mirror port only receive the traffic from the port being monitored, so the interface connected to that port becomes unusable to access the network. Again I was using ubuntu 18.04 on my intel NUC computer.

The NUC computer has both wifi and ethernet. Whenever I turned on the mirroring on the port connected to the ethernet interface of the NUC, the computer would loose all connectivity to the network.

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

I [never figured out](https://askubuntu.com/questions/1088396/how-to-use-wifi-for-lan-and-internet-access-and-ethernet-for-traffic-monitoring) how to avoid. But went a different route: I got a usb ethernet device, and added a new interface, so I would not have to figure out how to prioritize the wifi interface and would probably be more efficient.

I had two more problems to solve... First the USB Interface came back with a really long name which contained the full MAC address in the name... This can be resolved by adding a `/etc/udev/rules.d/70-persistent-net.rules` files as such:

{% highlight bash %}
# usb interface
#

SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="00:XX:XX:XX:XX:XX", ATTR{dev_id}=="0x0", ATTR{type}=="1", NAME="enus
b1"
{% endhighlight %}

Next, it was somehow still prioritizing the wrong interface (the tap was in the usb interface and this ended up first). But I managed to sort this by entering explicitely in the /etc/network/interfaces file both interface name in the desired order and now all works as desired, they both have a zero metrics, but the order is fine, the enusb1 interface receives all the mirrored traffic, eno1 is the interface used to access the network and ntopng works fine!

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







