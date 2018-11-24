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

## Fixing ipv6

I had setup ipv6 on the controller by setting the default configuration for the wan and the lan as:

![wan](/assets/unifi_wan_setup.png)
![lan](/assets/unifi_lan_setup.png)

Unfortunately, my devices refused to connect via ipv6 and [ipv6-test.com](http://ipv6-test.com/) was reporting all failed.

Because it was all working on my previous edgerouter lite, I decided to compare the configuration in details. I extracted the configuration by downloading a backup from the edgerouter and inspecting the `config.boot` file. I compared it with the config.json files [extracted from the usg pro](https://help.ubnt.com/hc/en-us/articles/215458888-UniFi-USG-Advanced-Configuration) via `mca-ctrl -t dump-cfg`. The format being different, yaml vs json, made it a bit painful, but I found the few different in the `interfaces/ethernet/eth2/pppoe/0/` config, which can be tested by running the below on the usg pro directly:

{% highlight bash %}
configure
set interfaces ethernet eth2 pppoe 0 dhcpv6-pd pd 0 interface eth0 host-address ::1
set interfaces ethernet eth2 pppoe 0 dhcpv6-pd pd 0 interface eth0 service slaac   
commit
{% endhighlight %}

After running these, ipv6 started working on all the devices. Of course this will be lost at the next provision, but all that is needed is to add these to the config.gateway.json on the controller, with the following :

{% highlight bash %}
{
  "interfaces" : {
    "ethernet" : {
      "eth2" : {
        "pppoe" : {
          "0" : {
            "dhcpv6-pd" : {
              "pd" : {
                "0" : {
                  "interface" : {
                    "eth0" : {
                      "host-address" : "::1",
                      "service" : "slaac"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  },	
}
{ endhighlight %}

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







