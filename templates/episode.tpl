{% extends "base.tpl" %}

{% block body %}
<div class="episode"><h3 class="summary"{% if header_color is defined %} style="border-bottom:3px solid #{{header_color}};"{% endif %}><a class="url" href="/{{site|d("error")}}/{{episode.link|d('#')}}">{{episode.name|d("episode.name")}}</a></h3><small class="author">{{episode.author|d("episode.author")}}</small><small class="date"> @ {{episode.date|d("episode.date")}}</small><div class="news">
  <p class="">{{episode.short|d("episode.short")}}</p>
  <p class="">{{episode.long|d("episode.long")}}</p>
  <ul class="">
  {% for f in files|d([]) %}<li><a href="{{f.link}}">{{f.name}}</a> {{f.info}}</li>{% endfor %}
  </ul>
</div>
</div>
<div class="comments">
<p>{% set comments = comments|d([]) %}{{comments|count}} Comment{{comments|count != 1 and "s" or ""}}</p>
{% for comment in comments %}<div class="comment">{{comment.text}}<br/><small class="author">{{comment.author}}</small><small class="date"> added these pithy words on {{comment.date}}</small></div>{% endfor %}

<form action="/{{site}}/{{episode.link}}/comment/new" method="post" id="commentform">
<input name="submit" id="submit" type="submit" tabindex="5" value="Say It!" style="position:absolute;margin-left:29em;" />
	<p>
	  <input type="text" name="author" id="author" class="textarea" value="" size="15" tabindex="1" />
	   <label for="author">Name</label> (required)
	</p>

	<p>
	  <input type="text" name="email" id="email" value="" size="15" tabindex="2" />
	   <label for="email">E-mail</label> (required)	</p>

	<p>
	  <label for="comment">Your Comment</label>
	<br />
	  <textarea name="comment" style="border: 1px solid #000;" id="comment" cols="50" rows="6" tabindex="4"></textarea>
	</p>
	  
	</form>


</div>
{% endblock %}

