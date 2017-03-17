# i cry while u sleep
but also while you're awake

{% assign post = site.posts.first %}
 <a href="{{ post.url | prepend: site.github.url }}">
      {{ post.title }}
      {{ post.content |truncatehtml | truncatewords: 60 }}


### buttons here
{%assign firstpost = site.posts.last %}
 <a href="{{ post.url | prepend: site.github.url }}"> First
 Oh wait maybe some pagination
 

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
