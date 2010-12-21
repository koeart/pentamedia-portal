{% extends "astro.tpl" %}
{% from "comments.tpl" import print_comments with context %}
{% from "rating.tpl"   import print_rating   with context %}

{% block body %}
      <p class="date">{{episode.author|d("episode.author")}} @ {{episode.fdate()|d("episode.date")}}</p>
      <h2>{{episode.name|d("episode.name")}}</h2>
      <div class="stars" style="margin-top:-1em;color:#{% if rating.count == 0 %}ccc{% else %}777{% endif %}">{{rating.stars}}</div>

  <div style="clear:both;margin:0em auto;max-width:70%;padding-left:20%;height:300px">
    <div class="screen pane" style="float:left">
      <img src="{{preview and preview.poster or '/img/empty_screen.jpg'}}" width="360" height="270" class="screen" />
    </div>
    <div class="download pane" style="margin:1em auto">
      <h3>Download</h3>
        <dl>
        {% for f in files %}
        <dh><a href="{{f.link}}"
            type="application/{{f.type}}" class="mime"
            rel="enclosure">{{f.name}}</a></dh>
        <dd>{{f.info}}</dd>{% endfor %}
      </dl>
    </div>
  </div>

      <div class="actions">
<p>&nbsp;</p>
    <p>
    Wir freuen uns über Feedback: bitte
    an <a href="mailto:mail@c3d2.de">mail@c3d2.de</a>, <a href="http://identi.ca/pentaradio">@pentaradio (identi.ca)</a>
    oder an <a href="http://twitter.com/pentaradio">@pentaradio (twitter)</a> schicken, denten oder tweeten.
    </p>

<p>&nbsp;</p>
{{print_rating()}}
{{print_comments()}}
<br/>
{% for tb in trackbacks %}
  <div class="comment">{{tb.text or ""}}
    <small><b><a href="{{tb.url}}">{{tb.title or "---"}}</a></b> by {{tb.name or "Unknown"}} on {{tb.fdate()}}</small>
  </div>
{% endfor %}

</div>

<div style="position:absolute;right:3px;"><small><a href="/{{site}}/{{episode.link}}/comments.atom">Atom</a></small></div>

{% endblock %}
