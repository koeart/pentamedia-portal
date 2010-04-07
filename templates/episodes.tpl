{% extends "base.tpl" %}

{% block body %}
{% for episode in episodepage|d([]) %}
<div class="sendung"><h3 class="news_summary"{% if header_color is defined %} style="border-bottom:3px solid #{{header_color}};"{% endif %}><a class="url" href="/{{site}}/{{episode.link|d('#')}}">{{episode.name|d("episode.name")}}</a></h3><small class="news_author">{{episode.author|d("episode.author")}}</small><small class="news_date"> @ {{episode.date|d("episode.date")}}</small><div class="news">
  <p class="">{{episode.short|d("episode.short")}}</p>
</div>
</div>
{% endfor %}

{% endblock %}

