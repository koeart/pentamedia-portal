{% extends "base.tpl" %}

{% block body %}
<form action="login" method="post" id="loginform">
	<p>
	  <input type="text" name="name" id="name" class="textarea" value="" size="15" tabindex="1" />
	   <label for="name">OpenID Account</label> (required) </p>
	<p>
    <input name="submit" id="submit" type="submit" tabindex="5" value="Let me in!" />
  </p>
	</form>
{% endblock %}
