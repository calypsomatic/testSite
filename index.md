## i cry while u sleep
but also while you're awake

{% assign post = site.posts.first %}
 <a href="{{ post.url | prepend: site.github.url }}">
      {{ post.title }}
      {{ post.content |truncatehtml | truncatewords: 60 }}


![OK THIS IS THE ONE]({{site.github.url}}/assets/bad.jpeg)
### buttons here

image here

### buttons here

comments here

links on the sidebar?

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url | prepend: site.github.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
