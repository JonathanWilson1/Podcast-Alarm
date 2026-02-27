---
layout: default
title: Blog
permalink: /blog/
---

<div class="container py-4">
  <h1 class="mb-4">Blog</h1>

  <div class="row">
    {% for post in site.posts %}
    <div class="col-md-4 mb-4">
      <div class="card h-100">
        <a href="{{ post.url }}">
          <img src="{{ post.featured-image }}" class="card-img-top" alt="{{ post.featured-image-alt }}" />
        </a>
        <div class="card-body d-flex flex-column">
          <small class="text-muted mb-1">{{ post.categories }}</small>
          <a href="{{ post.url }}"><h5 class="card-title">{{ post.title }}</h5></a>
          <p class="card-text text-muted" style="font-size: 0.85em;">{{ post.description | truncate: 120 }}</p>
          <small class="text-muted mt-auto">By {{ post.author }}</small>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
