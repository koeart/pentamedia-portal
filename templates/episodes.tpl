{% extends "astro.tpl" %}

{% block body %}
{% for episode, comment_count in episodepage|d([]) %}
<div class="episode">
  <h3 class="summary">
    <a class="url" href="/{{site}}/{{episode.link|d('#')}}">{{episode.name|d("episode.name")}}</a>
  </h3>
  <small class="date">
    {% if comment_count != 0 %}{{comment_count}} Comment{{comment_count != 1 and "s" or ""}} :: {% endif %}
    <em>{{episode.author|d("episode.author")}}</em> @ {{episode.fdate()|d("episode.date")}}
  </small>
  <div class="news">
    <p class="">{{episode.short|d("episode.short")}} <a class="url" href="/{{site}}/{{episode.link|d('#')}}">more…</a></p>
  </div>
</div>
{% endfor %}

{% endblock %}

