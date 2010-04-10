{% extends "base.tpl" %}

{% block body %}
<div style="text-align:center;">
  <form action="submit" method="post" id="submitform">
    <textarea name="blob" id="blob" cols="42" rows="2" tabindex="1"></textarea>
    <input name="submit" id="submit" type="submit" tabindex="2" value="add this!" />
	</form>
</div>
<br/>
{% for entry in entries() %}<div class="entry"><a href="{{entry.url}}">{{entry.title|e}}</a><br/><small>{{entry.description|e}}</small><p>{{entry.excerpt|e}}</p></div>{% endfor %}
{% endblock %}
