{% extends "astro.tpl" %}
{% from "comments.tpl"import print_comments with context %}

{% block body %}
      <p class="date">{{episode.author|d("episode.author")}} @ {{episode.fdate()|d("episode.date")}}</p>
      <h2>{{episode.name|d("episode.name")}}</h2>

      <div class="description">
	<p><em>{{episode.short|d("episode.short")}}</em></p>
	<p>{{episode.long|d("episode.long")}}</p>
	<p>
	  Wir freuen uns über Feedback: bislang bitte
	  an <a href="mailto:mail@c3d2.de">mail@c3d2.de</a> schicken
	  oder <a href="http://twitter.com/pentaradio">@pentaradio</a>

	  tweeten.
	</p>

{{print_comments()}}
<br/>
{% for tb in trackbacks %}
  <div class="comment">{{tb.text or ""}}
    <small><b><a href="{{tb.url}}">{{tb.title or "---"}}</a></b> by {{tb.name or "Unknown"}} on {{tb.fdate()}}</small>
  </div>
{% endfor %}

      </div>
 {% if files|d([]) != [] %}
      <div class="actions">
	<div class="download pane">
	  <h3>Download</h3>
	  <dl>
	    {% for f in files %}
	    <dh><a href="{{f.link}}"
		   type="application/{{f.type}}" class="mime"
		   rel="enclosure">{{f.name}}</a></dh>
	    <dd>{{f.info}}</dd>{% endfor %}
	  </dl>
	</div>
	<div class="listen pane" id="penta{{site}}">
	  <h3>Hören</h3>
	  <video controls="controls">
	    {% for f in files %}
	    <source src="{{f.link}}"
		    type="audio/{{f.type}}"/>{% endfor %}
	    Bitte Browser auf den neuesten Stand bringt. Hilft bei
	    Multimedia und Sicherheit!
	  </video>
	</div>
      </div>{% endif %}
 {% if links|d([]) != [] %}
      <div class="shownotes pane">
	      <p>Shownotes:</p>
	      <ul class="shownotes">
	        {% for link in links %}
	        <li><a href="{{link.url}}">{{link.title}}</a></li>{% endfor %}
	      </ul>
      </div>{% endif %}

<div style="position:absolute;right:3px;"><small><a href="/{{site}}/{{episode.link}}/comments.atom">Atom</a></small></div>

{% endblock %}
