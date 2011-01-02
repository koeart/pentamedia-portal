{% extends "astro.tpl" %}
{% from "comments.tpl" import print_comments with context %}
{% from "rating.tpl"   import print_rating   with context %}

{% block body %}


      <p class="date">{{episode.author|d("episode.author")}} @ {{episode.fdate()|d("episode.date")}}</p>
      <h2>{{episode.name|d("episode.name")}}</h2>
      <div class="stars" style="margin-top:-1em;color:#{% if rating.count == 0 %}ccc{% else %}777{% endif %}">{{rating.stars}}</div>

  <div style="clear:both;margin:0em auto;max-width:70%;padding-left:20%;height:300px">
    <div class="screen pane" style="float:left">
      <div class="frame">
      {% if preview|d(False) %}
      <!-- Begin VideoJS -->
        <div class="video-js-box vim-css">
          <video class="video-js" width="360" height="202" poster="{{preview.static}}" preload="none" controls>
            {% for f in files %}
              <source src="{{f.link}}" type='video/{{f.type}}' />
            {% endfor %}
            <object id="flash_fallback_1" class="vjs-flash-fallback" width="360" height="202" type="application/x-shockwave-flash" data="http://releases.flowplayer.org/swf/flowplayer-3.2.1.swf">
              <param name="movie" value="http://releases.flowplayer.org/swf/flowplayer-3.2.1.swf" />
              <param name="allowfullscreen" value="true" />
              <param name="flashvars" value='config={"playlist":["{{preview.static}}", {"url": "{{files[0].link}}","autoPlay":false,"autoBuffering":true}]}' />
                <img src="{{preview.animated}}" alt="Poster Image" title="No video playback capabilities." class="animated screen" />
            </object>
          </video>
          <p class="vjs-no-video" style="color:white">Video not playable with <a href="http://videojs.com">HTML5 Video Player</a>.</p>
        </div>
      <!-- End VideoJS -->
      {% else %}
        <img src="/img/empty_screen.jpg" class="static screen" />
        <img src="/img/empty_screen.jpg" class="animated screen" />
      {% endif %}
      </div>
    </div>
    <div class="download pane" style="margin:1em auto">
      <h3>Download</h3>
        <dl>
        {% for f in files %}
        <dh><a href="{{f.link}}"
            type="video/{{f.type}}" class="mime"
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

{% if preview|d(False) %}
<script src="/js/jquery-1.4.4.min.js" type="application/javascript" defer="defer"></script>
<script src="/video-js/video.js" type="text/javascript" charset="utf-8"></script>
<script type="text/javascript" charset="utf-8">

  // Add VideoJS to all video tags on the page when the DOM is ready
  VideoJS.setupAllWhenReady({
      showControlsAtStart: true,
      controlsBelow: false,
      controlsHiding: true,
      linksHiding: false
  });

</script>
{% endif %}

{% endblock %}
