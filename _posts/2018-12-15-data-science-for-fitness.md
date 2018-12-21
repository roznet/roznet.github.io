---
layout: post
title:  "Data Science for Fitness"
date:   2018-12-15 18:02:13 +0100
categories: "Data"
comments: true
---

I am now trying to learn more about data science. Instead of looking at random examples in the books or data sets in kaggle, I told myself: why not try to apply new techniques on my fitness data. This could be an interesting way to both learn and enhance [ConnectStats](https://github.com/roznet/connectstats).

So here we go and this is the first post on the serie. Hopefully it won't be the last.

# How to load the data

Of course, my initial approach was to download the sqlite files ConnectStats saves, load that into pandas from jupyter and start looking at an activity, which was quick, and I was starting to picture bringing all the sqlite files from the phone and loading them sequentially to explore the learning libraries in python. 

But this being a hobby and not a job with deadline, I decided to take a detour and build something so that I can make it easier for other to do analysis on their health data as well. Who knows, hopefully other people interesting in data science may want to help and contribute ideas and analysis to use in the app.

So decided to enhance FitFileExplorer to make it easier from a computer to access the require data via fit files and generate the required sharded pieces to be brought all together in the jupyter notebook for analysis.

Major distraction from the original goal, but as I say, this is not a job, but a hobby, so why not :)

# First Detour

My first idea was to leverage the code of ConnectStats and to try to get the iOS code to compile in the MacOS app. Sounds simple. Turned out to be a massive pain. I had not abstracted enough all the component about parsing activities and it started to require to bring way to many files, including a lot of infrastructure to maintain profiles, calculations, database support, multi format import, etc which was a big overkill for the MacOS app. It felt like pulling a string hoping it would be short and realizing that a whole bundle of spaghetti would have to come with it or a major refactoring would be necessary. Too much. Even for a hobby...

So I decided to just implement just the minimum to download fit file and reformat them in bulk into `csv` or other appropriate format for import to jupyter and data science tools.

Easy enough, I have the basics working now. 

**BUT** for the parsing of the Fit file, I had been using the c++ library from the [Fit SDK](https://www.thisisant.com/resources/fit). And while on opening one file it was a bit slow, I had not realize just how slow it was until I try to parse several files. 

# Second Detour

So I had the option of writing the code, and letting the download go and letting the parsing take the 5+ hours I was estimating and get on with my goal of analysing the data. Or work at optimizing the parsing to be much faster. A few weeks late, I now have a much [faster proof of concept code](https://github.com/roznet/fit-sdk-swift) in swift that do the parsing of a file that use to take 7 seconds in 0.04 seconds... And of course I still have to finish the integration into Fit File Explorer and get the data fully prepared for analysis... 

Worth it.

See the next post to learn about [Fast Fit File Parsing]({% post_url 2018-12-20-faster-fit-parsing %})...
