# i cry while u sleep
but also while you're awake

{% assign latest = site.posts.first %}
 <a href="{{ latest.url | prepend: site.github.url }}">
      {{ latest.title }}
      {{ latest.content }}


### buttons here
{%assign firstpost = site.posts.last %}
{%assign prev = firstpost.previous%}
{%assign next = firstpost.next%}
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
