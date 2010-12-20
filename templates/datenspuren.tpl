{% extends "astro.tpl" %}
{% from "comments.tpl" import print_comments with context %}
{% from "rating.tpl"   import print_rating   with context %}

{% block body %}


      <p class="date">{{episode.author|d("episode.author")}} @ {{episode.fdate()|d("episode.date")}}</p>
      <h2>{{episode.name|d("episode.name")}}</h2>
      <div class="stars" style="margin-top:-1em;color:#{% if rating.count == 0 %}ccc{% else %}777{% endif %}">{{rating.stars}}</div>

{% for episode, comment_count, rating in episodepage|d([]) %}
<div class="episode">
  <h3 class="summary">
    <a class="url" href="/{{full_site}}/{{episode.link|d('#')}}">
      {{episode.name|d("episode.name")}}
      {% if episode.filescount %}<span style="font-size:0.6em">{{episode.filescount}}</span>{% endif %}
    </a>
  </h3>
  <small class="date">
    {% if comment_count != 0 %}{{comment_count}} Comment{{comment_count != 1 and "s" or ""}} :: {% endif %}
    <em>{{episode.author|d("episode.author")}}</em> @ {{episode.fdate()|d("episode.date")}}
    <span class="stars"{% if rating.count == 0 %} style="color:#ccc"{% endif %}>
      <span style="font-size:0.6em">{{rating.count|d(0)}}</span>
      {{rating.stars|d("rating.stars")}}
    </span>
  </small>
  {% if episode.has_screen|d(False) %}
  <div style="clear:both;margin:0em auto;max-width:70%;padding-left:20%;height:300px">
    <div class="screen pane" style="float:left">
      <img src="/img/empty_screen.jpg" width="360" height="270" class="screen" />
    </div>
    <div class="download pane" style="margin:1em auto">
      <h3>Download</h3>
        <dl>
        {% for f in episode.files %}
        <dh><a href="{{f.link}}"
            type="application/{{f.type}}" class="mime"
            rel="enclosure">{{f.name}}</a></dh>
        <dd>{{f.info}}</dd>{% endfor %}
      </dl>
    </div>
  </div>
  {% endif %}
</div>
{% endfor %}

<p>&nbsp;</p>
<h3>{{episode.name|d("episode.name")}}</h3>
{{print_rating()}}
{{print_comments()}}
<p>&nbsp;</p>

<div style="position:absolute;right:3px;"><small><a href="/{{full_site}}/comments.atom">Atom</a></small></div>

{% endblock %}

