{% extends "astro.tpl" %}

{% block body %}
      <p class="date">{{episode.author|d("episode.author")}} @ {{episode.date|d("episode.date")}}</p>
      <h2>{{episode.name|d("episode.name")}}</h2>

      <div class="description">
	<p>{{episode.short|d("episode.short")}}</p>
	<p>{{episode.long|d("episode.long")}}</p>
	<p>
	  Wir freuen uns über Feedback: bislang bitte
	  an <a href="mailto:mail@c3d2.de">mail@c3d2.de</a> schicken
	  oder <a href="http://twitter.com/pentaradio">@pentaradio</a>

	  tweeten.
	</p>
	
<div class="comments">
<p>{% set comments = comments|d([]) %}{{comments|count}} Comment{{comments|count != 1 and "s" or ""}}</p>
{% for comment in comments %}
  <div class="comment"{% if comment.reply != -1 %} style="padding-left:10px;border-left:4px solid #ddd;"{% endif %}>{{comment.text}}
    <small class="author"><a href="/{{site}}/{{episode.link}}/reply?{{comment.id}}#new" class="line">{{comment.author|trim|e}}</a></small>
    <small> added these pithy words on {{comment.date}}</small>
  </div>
{% endfor %}
{% if comment_form %}
<form action="/{{site}}/{{episode.link}}/comment/new" method="post" id="new">
<input type="hidden" name="hash" value="{{hash}}" />
<input type="hidden" name="reply" value="{{reply}}" />
<input name="submit" id="submit" type="submit" tabindex="5" value="Say It!" style="position:absolute;margin-left:29em;" />
	<p>
	  <input type="text" name="author" id="author" class="textarea" value="" size="15" tabindex="1" />
	   <label for="author">Name</label> (required)
	</p>

	<p>
	  Enter the sum of {{a}}, {{b}} and {{c}}:
	  <input type="text" name="captcha" id="captcha" value="" size="3" tabindex="2" />
	   <label for="email">SumCaptcha</label> (required)	</p>
	<p>
	  <label for="comment">Your Comment</label>
	<br />
	  <textarea name="comment" style="border: 1px solid #000;" id="comment" cols="50" rows="6" tabindex="4">{{at_author}}</textarea>
	  <br /><a href="http://en.wikipedia.org/wiki/Markdown">Markdown</a> enabled. (url autolinking included.)
	</p>
	  
	</form>
{% else %}
<a href="/{{site}}/{{episode.link}}/comment#new" class="add_comment">new Comment …</a>
{% endif %}
</div>
	
      </div>
     
      <div class="actions">
	<div class="download pane">
	  <h3>Download</h3>
	  <dl>
	    {% for f in files|d([]) %}
	    <dh><a href="{{f.link}}"
		   type="application/{{f.type}}" class="mime"
		   rel="enclosure">{{f.name}}</a></dh>
	    <dd>{{f.info}}</dd>{% endfor %}
	  </dl>
	</div>
	<div class="listen pane" id="penta{{site}}">
	  <h3>Hören</h3>
	  <video controls="controls">  
	    {% for f in files|d([]) %}
	    <source src="{{f.link}}"
		    type="audio/{{f.type}}"/>{% endfor %}
	    Bitte Browser auf den neuesten Stand bringt. Hilft bei
	    Multimedia und Sicherheit!
	  </video>  
	</div>
      </div>
 
      <div class="shownotes pane">
	<p>Shownotes:</p>
	<ul class="shownotes">
	  <li><a href="">link</a></li>
	</ul>
      </div>
{% endblock %}
