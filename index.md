# i cry while u sleep
but also while you're awake

{% assign thispost = site.posts.first %}
 <a href="{{ thispost.url | prepend: site.github.url }}">
      {{ thispost.title }}
      {{ thispost.content }}


### buttons here
{%assign firstpost = site.posts.last %}
{%assign prev = thispost.previous%}
{%assign next = thispost.next%}
{% assign latest = site.posts.first %}
 <a href="{{ firstpost.url | prepend: site.github.url }}"> First
 <a href="{{ prev.url | prepend: site.github.url }}"> Prev
 <a href="{{ next.url | prepend: site.github.url }}"> Next
 <a href="{{ latest.url | prepend: site.github.url }}"> Latest
 

comment?
patreon link?
sidebar?

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url | prepend: site.github.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
