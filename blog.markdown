---
layout: default
title: Blog
permalink: /blog/
---

<div class="container">

<div class="row">
{% for post in site.posts limit:1 %}
    {% include blogPostItemFullRow.html %}
{% endfor %}
</div>

<div class="row">
{% for post in site.posts offset:1 limit:3 %}
  <div class="col-sm d-flex align-items-stretch">
    {% include blogPostItem.html %}
  </div>
{% endfor %}
</div>

<br/>

{% for post in site.posts offset:4 limit:2 %}
<div class="row">
  <div class="col-sm d-flex align-items-stretch">
    {% include blogPostItemHalfRow.html %}
  </div>
</div>
{% endfor %}

<div class="row">
{% for post in site.posts offset:6 limit:3 %}
  <div class="col-sm d-flex align-items-stretch">
    {% include blogPostItem.html %}
  </div>
{% endfor %}
</div>

<br/>
{% for post in site.posts offset:9 %}
<div class="row">
  <div class="col-sm d-flex align-items-stretch">
    {% include blogPostItemHalfRow.html %}
  </div>
</div>
{% endfor %}

</div>
