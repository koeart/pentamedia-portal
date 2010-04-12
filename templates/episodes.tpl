{% extends "base.tpl" %}

{% block body %}
{% for episode, comment_count in episodepage|d([]) %}
<div class="episode">
  <h3 class="summary"{% if header_color is defined %} style="border-bottom:3px solid #{{header_color}};"{% endif %}>
    <a class="url" href="/{{site}}/{{episode.link|d('#')}}">{{episode.name|d("episode.name")}}</a>
  </h3>
  <small class="author">{{episode.author|d("episode.author")}}</small>
  <small class="date"> @ {{episode.date|d("episode.date")}}</small>
  {% if comment_count != 0 %}<small class="comments"> :: {{comment_count}} Comment{{comment_count != 1 and "s" or ""}}</small>{% endif %}
  <div class="news">
    <p class="">{{episode.short|d("episode.short")}} <a class="url" href="/{{site}}/{{episode.link|d('#')}}">more…</a></p>
  </div>
</div>
{% endfor %}

{% endblock %}

