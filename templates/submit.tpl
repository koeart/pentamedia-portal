{% extends "base.tpl" %}

{% block body %}
<form action="add" method="post" id="loginform">
	<p><input type="text" name="title" id="title" class="textarea" value="{{url_title|d('')}}" size="42" tabindex="1" />
	   <label for="title">Title</label></p>
	<p><input type="text" name="url" id="url" class="textarea" value="{{url|d('')}}" size="42" tabindex="2" />
	   <label for="url"><label for="url"><acronym title="Uniform Resource Locator">URL</acronym></label></p>	   
	<p><textarea name="description" id="description" cols="42" rows="1" tabindex="3"></textarea>
	   <label for="description">Description</label></p>	   
	<p><textarea name="excerpt" id="excerpt" cols="42" rows="6" tabindex="4">{{excerpt|d("")}}</textarea>
	   <label for="excerpt">Excerpt</label></p>	   
	<p><input type="text" name="tags" id="tags" class="textarea" value="" size="42" tabindex="5" />
	   <label for="tags">Tags</label> (separated by spaces)</p>
	<p>
    <input name="submit" id="submit" type="submit" tabindex="6" value="Do it!" />
  </p>
	</form>
{% endblock %}
