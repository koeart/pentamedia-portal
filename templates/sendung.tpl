{% extends "base.tpl" %}

{% block body %}
<div class="sendung"><h3 class="news_summary"{% if header_color is defined %} style="border-bottom:3px solid #{{header_color}};"{% endif %}><a class="url" href="/{{site|d("error")}}/{{episode.link|d('#')}}">{{episode.name|d("episode.name")}}</a></h3><small class="news_author">{{episode.author|d("episode.author")}}</small><small class="news_date"> @ {{episode.date|d("episode.date")}}</small><div class="news">
  <p class="">{{episode.short|d("episode.short")}}</p>
  <p class="">{{episode.long|d("episode.long")}}</p>
</div>
</div>
<div class="comments">
{% for comment in comments|d([]) %}<div class="comment">comment here</div>{% endfor %}
</div>
{% endblock %}

