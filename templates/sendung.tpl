{% extends "base.tpl" %}

{% block body %}
<div class="sendung"><h3 class="news_summary"{% if header_color is defined %} style="border-bottom:3px solid #{{header_color}};"{% endif %}><a class="url" href="{{episode_link|d('#')}}">{{episode|d("episode")}}</a></h3><small class="news_author">{{author|d("author")}}</small><small class="news_date"> @ {{date|d("date")}}</small><div class="news">
  <p class="">{{short_text|d("short text")}}</p>
  <p class="">{{long_text|d("long text")}}</p>
</div>
</div>
<div class="comments">
{% for comment in comments|d([]) %}<div class="comment">comment here</div>{% endfor %}
</div>
{% endblock %}

