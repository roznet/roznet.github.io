---
layout: post
title:  "Adding a word cloud thumbnail to post titles in jekyll"
date:   2018-12-09 13:50:13 +0100
categories: web
comments: true
---

I love word cloud. As I have just started a site with jekyll I wondered how would it look to add a word cloud thumbnail to the list of post as a thumbnail and how hard would it be?

## Building the word cloud images

My first instinct was to see if there was a python package to build wordcloud. I know python quite well, and would definitely be easy to automate the generation of the images. And of course python has usually pretty much any type of [module you can ever dream of](https://xkcd.com/353/), so felt like a good start.

A quick web search later and of course, there is a very nice and easy to [use package](http://amueller.github.io/word_cloud/) already. Install into my anaconda setup was trivial with `conda install -c conda-forge wordcloud`.

It was then trivial to loop through the posts files and generate a corresponding word cloud image for each

```python
for fn in allposts:
    if fn.endswith(".md") and os.path.isfile(fn):
        fp = open( post_dir + fn,'r')
        text = fp.read()
        wordcloud = WordCloud(max_words=30,background_color=(21,21,21)).generate(text)
        outname = img_dir + fn[:-len('md')] + 'png'
        wordcloud.to_file(outname)
```
I just picked the background color to match the background I had set in my jekyll site theme.

I set the `img_dir` to be a subfolder `/assets/clouds` in the side, et voila, the thumbnails were ready.

## Adding the thumbnail to the list of posts

Next step was to figure out how to automatically add the image to the list of post. For that I had to find out a bit more about which [liquid tag and filters](https://jekyllrb.com/docs/liquid/filters/)  were available.

It was actually quite simple to generate the thumbnail file name replacing the prefix by the path with the images and the suffix with png

```html
{% raw %}{% assign filename = post.path | remove_first: '_posts/' | replace: '.md', '.png' | prepend: '/assets/clouds/' %}{% endraw %}
```

I also wanted to make sure if the png didn't exist that the generation would just skip the image. I found out that there was a `site.static_files` variables that could help, I just had to iterate through that and see if the required image was found. Which resulted in the following code in my `home.html` template:

```html
{% raw %}
      <li>
        {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
	{% assign filename = post.path | remove_first: "_posts/" | replace: '.md', '.png' | prepend: "/assets/clouds/" %}
	{% for static_file in site.static_files %}
	{% if static_file.path == filename %}
	<a href="{{ post.url | relative_url }}"><img src="{{ filename }}" width="120px" /></a>
	{% endif %}
	{% endfor %}
	
        <span class="post-meta">{{ post.date | date: date_format }}</span>
        <h3>
          <a class="post-link" href="{{ post.url | relative_url }}">
            {{ post.title | escape }}
          </a>
        </h3>
{% endraw %}
```

The last stage was to work out how to get the thumbnail properly placed to the left in the list

## Positioning the thumbnail

This turned out quite trivial to do, after a quick web search. As expected a list with thumbnail is quite a common occurence on the way. Just required a few lines edit to the `_layout.scss` file in the post-list class to specify to float the `img` under `li` and add a margin

```css
.post-list {
  li img {
      float: left;
      margin: 0 15px 0 0;
  }
}
```

## Automating the generation

The last piece was to automate the process of generating the word cloud images. Easiest way was to create a small python script and a make file to achieve that.
I created a new directory `_bld` in my [website repo](https://github.com/roznet/roznet.github.io), and simple makefile

```make
POST_FILES=$(shell find $(POST_DIR) -type f -name *.md)
IMG_FILES=$(patsubst $(POST_DIR)/%,$(IMG_DIR)/%,$(POST_FILES:.md=.png))

all: $(IMG_FILES)

$(IMG_DIR)/%.png: $(POST_DIR)/%.md
	./gencloud.py -o $(IMG_DIR) $<
```

You can see the final code in my [website repo](https://github.com/roznet/roznet.github.io) and how the list looks [here](https://roznet.github.io)