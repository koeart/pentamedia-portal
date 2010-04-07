{% extends "base.tpl" %}

{% block body %}
<div class="sendung"><h3 class="news_summary"{% if header_color is defined %} style="border-bottom:3px solid #{{header_color}};"{% endif %}><a class="url" href="/{{site|d("error")}}/{{episode.link|d('#')}}">{{episode.name|d("episode.name")}}</a></h3><small class="news_author">{{episode.author|d("episode.author")}}</small><small class="news_date"> @ {{episode.date|d("episode.date")}}</small><div class="news">
  <p class="">{{episode.short|d("episode.short")}}</p>
  <p class="">{{episode.long|d("episode.long")}}</p>
</div>
</div>
<div class="comments">
{% for comment in comments|d([]) %}<div class="comment">{{comment.text}}<br/>{{comment.author}} @ {{comment.date}}</div>{% endfor %}

<form action="/{{site}}/{{episode.link}}/comment/new" method="post" id="commentform">

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

	<p>

	  <input name="submit" id="submit" type="submit" tabindex="5" value="Say It!" />
	</p>
	</form>


</div>
{% endblock %}

