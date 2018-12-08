---
layout: post
title: "Troubleshooting network issues"
date: 2018-11-12 11:38:00 +0100
category: network
---
One of the requirement for me in finding a new house was to make sure it had ethernet cabling everywhere so I could ensure I have a stable network and enough access point to get good wifi connectivity in every room.

When I moved into a new place in August 2016, it met the requirement, but to my and my family dismay, the network and wifi stability was dreadful. It consistently would stall time and time over again. Streaming movies or music want halt for minutes at a time, and reading news on the web would also randomly hang.

I embarked on a long journey to try to resolve the issue, which would lead me to learn way more about networking that I ever imagined possible...

## December 2016: The ISP Router

My first guess was that the culprit was my BT router. Though I had moved my line and all my equipment from my previous house where everything was working fine, I suspected that the issue could first be the router being of an older generation that had issue keeping the line. BT at the time offered a new router that supported IPV6, so I figured maybe upgrading that would solve the issue.

It didn't change much and the network connectivity continued to be very poor.

## February 2017: Wifi interference

In my new house, I could see many wifi networks from the neighbors, so I started to suspect that the problem may be interference and my old netgear access point were overwhelmed.

I wasn't using the BT router as a wifi access point, because the BT line arrives in the basement and that was too out of the way, I had two older Netgear access point in the house connected via the ethernet cabling.

So I decided to upgrade to new Netgear R7000 router that I would setup as access points and added a managed Netgear ProSafe switch in the basement to make sure the issue wasn't from the BT router at all.

While this helped ensure that the signal strengh was very strong in all the rooms, somehow the network poor performance continued.

## June 2017: It must be the line

I became then convinced that the problem was the BT line itself. (Spoiler: I was wrong). And colleagues at work told me about AAISP, the provider that was [shibboleet](https://xkcd.com/806/) compliant. I called them and discussed my problem, they told me that I could switch to them, they have rigourous monitoring of the lines and if it was defective would help me sort it out. I made the switch.

I can't recommend AAISP more. They are great. There support is top notch. They have [control pages](https://support.aa.net.uk/CQM_Graphs) that provides great historical insights on what happened on your line.

And sure enough, their graphs showed constant drop of the lines for few minutes at a time. I was very excited. Finally a diagnostic that was showing a problem, and AAISP support told me something was definitely wrong and they would help me chase BT to fix the line. But the first thing I had to do is make sure I connected the router to the "test port" of the BT socket to make sure it wasn't an issue with my internal wiring.

My socket wasn't standard and didn't have a test port! BT would not look at my line until I could show the problem by connecting to that test port. Not to worry, I hired a technician to upgrade my socket to a new standard one and connected the router to the test socket.

This lead to the problem on the control graph disappearing all together. This was a new low. Now the line appeared to work perfectly, but the performance of my network was still as bad as before.

The AAISP technician told me it must be an issue with my router or network equipment. So I decided to upgrade the few remaining pieces (a few old switch) to newer one.

But this didn't resolve anything. And I started to worry it had to do with my internal wiring or ethernet cable. This prospect was concerning as I started to imagine ripping all the walls to find the cable problem.

## December 2017: Linux Server Monitor

So if it was an internal cabling issue, I had to try to narrow it down. It couldn't be all the cables and hopefully I would see which part of the network was the problem.

I decided to go to the next phase and after some research online decided to try to narrow down the problem by implementing some probes on my network using ping. First I tried to build a little python script from my imac that would ping a few devices regularly to see when the latency would change. This clearly showed some issue, but the script wasn't reliable and it seemed to be on every part of the network.

I then decided to move on to getting a small linux server and put some monitoring software on it. First, I hoped it would help me narrow down the problem further, and second, I wanted to get into linux.

I ordered a [NUC computer](https://www.intel.com/content/www/us/en/products/boards-kits/nuc.html). These are great little piece of hardware, reasonably priced and perfect to be left headless next to my main switch and router as a server/monitor. I installed ubuntu on it and among other tools, installed [smokeping](https://oss.oetiker.ch/smokeping/). I configured it to ping from the linux server to most hardware equipement (switches, access points, computer) in my network to see if one part of the network was the problem.

The graphs were dreadful, a lot of "dark" smoke and many dropped packets. Though far from 100% loss, the network was somewhat working but no single device was the issue: Everything was dark!

## January 2018: Upgrade of the last switch

Completely out of ideas, I decided to upgrade the last older switch I had to a new one. Not that I believed at that point it would help much, but I really didn't know what to do anymore and was secretely hoping the problem was a single defective device.

This didn't help of course, the performance continued to dreadful and the smokeping graphs remained stubornly dark throughout the network.

But upgrading that last switch, ultimately led me to the solution...

## February 2018: Epiphany!

After upgrading that last switch I noticed that the imac, hardwired by ethernet, I was using to log in remotely to my linux server started to behave much worse than before. While devices on wifi were always showing the worst network performance, the hardwired computer also but to a less extent. Though, after upgrading that last switch, to which the imac was connected, performance became very clearly worse. The connection to the linux server would constantly drop or stall.

So getting a new switch made things worse to my imac? What gives?

I reviewed the connection of the switched and realized that I had forgotted to connect the switch to the wall ethernet socket!

How was this possible? I could I have internet access while I had not connected the switch to the intranet???

This was the final clue! I have a Sonos system and one of the Sonos speaker is also connected to the switch and disconnecting the Sonos speaker dropped the internet all together.

Sonos is creating a mesh network over wifi (its own wifi, not my main network). After searching on this on the web, I found out that Sonos is using the [spanning tree protocol](https://en.community.sonos.com/troubleshooting-228999/sonos-and-the-spanning-tree-protocol-16973) to prevent loops. But then it occured to me that it must not work somehow with the netgear devices I had and creating intermittent random loops that lead to the network performance.

I found online information about [turning off the wifi](https://bsteiner.info/articles/disabling-sonos-wifi) on Sonos Devices as all my devices are also hardwired.

And since then, we enjoy top notch network and wifi performance in the house, partly thanks to all these upgrade network components :)

You can see on the smoke ping graph how clean the network is since that fix and compare to the dark smoke of the previous network situation...

![SmokePing](/assets/smokeping.png)

