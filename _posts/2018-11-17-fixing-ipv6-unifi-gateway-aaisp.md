---
layout: post
title:  "Fixing IPV6 with Unifi USG Gateway and AAISP"
date:   2018-11-17 09:57:13 +0100
categories: network
comments: true
---

My new unifi setup worked great, but somehow I was unable to get IPV6 working. I had an edgerouter before, so I knew the system should be compatible with my ISP.

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

After running these, ipv6 started working on all the devices. Of course this will be lost at the next provision, but all that was then needed is to add these to the config.gateway.json on the controller, with the following :

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
{% endhighlight %}

