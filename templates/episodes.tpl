{% extends "astro.tpl" %}

{% block body %}
{% for episode, comment_count, rating in episodepage|d([]) %}
<div class="episode">
  <h3 class="summary">
    <a class="url" href="/{{site}}/{{episode.link|d('#')}}">{{episode.name|d("episode.name")}}</a>
  </h3>
  <small class="date">
    {% if comment_count != 0 %}{{comment_count}} Comment{{comment_count != 1 and "s" or ""}} :: {% endif %}
    <em>{{episode.author|d("episode.author")}}</em> @ {{episode.fdate()|d("episode.date")}}
    <span class="stars"{% if rating.count == 0 %} style="color:#ccc"{% endif %}>{{rating.stars|d("rating.stars")}}</span>
  </small>
  <div class="news">
    <p class="">{{episode.short|d("episode.short")}} <a class="url" href="/{{site}}/{{episode.link|d('#')}}">more…</a></p>
  </div>
</div>
{% endfor %}

<div style="position:absolute;right:3px;"><small><a href="/{{site}}/comments.atom">Atom</a></small></div>

{% endblock %}

