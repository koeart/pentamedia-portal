{% extends "astro.tpl" %}
{% from "comments.tpl" import print_comments with context %}
{% from "rating.tpl"   import print_rating   with context %}

{% block body %}
      <p class="date">{{episode.author|d("episode.author")}} @ {{episode.fdate()|d("episode.date")}}</p>
      <h2>{{episode.name|d("episode.name")}}</h2>
      <div class="stars" style="margin-top:-1em;color:#{% if rating.count == 0 %}ccc{% else %}777{% endif %}">{{rating.stars}}</div>

      <div class="description">
	<p><em>{{episode.short|d("episode.short")}}</em></p>
	<p>{{episode.long|d("episode.long")}}</p>
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
 {% if files|d([]) != [] %}
      <div class="actions">
	<div class="download pane">
	  <h3>Download</h3>
	  <dl>
	    {% for f in files %}
	    <dh><a href="{{f.link}}"
		   type="application/{{f.typetyp()}}" class="mime {{f.mime()}}"
		   rel="enclosure">{{f.name}}</a></dh>
	    <dd>{{f.info}}</dd>{% endfor %}
	  </dl>
	</div>
	<div class="listen pane" id="penta{{site}}">
	  <h3>Hören</h3>

      <!-- Begin AudioJS -->
        <div class="audio-js-box vim-css" style="top:1.5em">
          <audio class="audio-js" width="360" height="0" style="height:0;border:none" preload="none" controls>
          Bitte Browser auf den neuesten Stand bringt. Hilft bei Multimedia und Sicherheit!
            {% for f in files %}
              <source src="{{f.link}}" type='{{f.type}}' />
            {% endfor %}
          </audio>
        </div>
      <!-- End AudioJS -->
	</div>
      </div>{% endif %}
 {% if links|d([]) != [] %}
      <div class="shownotes pane">
	      <h3>Shownotes</h3>
	      <ul class="shownotes">
	        {% for link in links %}
	        <li><a href="{{link.url}}">{{link.title}}</a></li>{% endfor %}
	      </ul>
      </div>{% endif %}

<div style="position:absolute;right:3px;"><small><a href="/{{site}}/{{episode.link}}/comments.atom">Atom</a></small></div>


<script src="/js/jquery-1.4.4.min.js" type="application/javascript" defer="defer"></script>
<script src="/js/rating-magic.js" type="application/javascript" defer="defer"></script>
<script src="/lib/audio-js/audio.js" type="text/javascript" charset="utf-8"></script>
<script type="text/javascript" charset="utf-8">

    // Add AudioJS to all video tags on the page when the DOM is ready
    window.onload = function(){
        var players = AudioJS.setup();
    };

</script>

{% endblock %}
