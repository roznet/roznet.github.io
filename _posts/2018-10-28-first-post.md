---
layout: post
title:  "First Post with Github Pages and Jekyll"
date:   2018-10-28 09:57:13 +0100
categories: web
---

So I have a blog/web page for connectstats and other app already, aimed at users, I have a twitter page, a facebook page and a github page. So why a new web site?

Well, this is really about learning jekyll and figuring out how to use github pages. Why? Well, my son was thinking about building a web site for a portfolio of his development activities, he is active on github so I advised him to try building it on github pages. Of course I have to drink my own coolaid and figure out how to use it too...

While it was easy to setup the site with the default theme, I was initially a bit confused how to customise it or change it.


## Changing the theme

I tried to change the theme from the default I had selected, [minima](https://github.com/jekyll/minima), to [hacker](https://github.com/pages-themes/hacker) and all stopped working, the site was blank.

The serve command was showing an error, which was somewhat confusing to the pure neophite I was in jekyll:

{% highlight bash %}
     Regenerating: 3 file(s) changed at 2018-11-11 16:39:53
                    _posts/2018-10-28-first-post.md
                    _posts/.#2018-10-28-first-post.md
                    _posts/#2018-10-28-first-post.md#
     Build Warning: Layout 'page' requested in about.md does not exist.
     Build Warning: Layout 'home' requested in index.md does not exist.
                    ...done in 0.096756 seconds.
 
{% endhighlight %}

