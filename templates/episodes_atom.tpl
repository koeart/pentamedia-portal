<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <author>
    <name>k-ot</name>
    <email>mail@c3d2.de</email>
    <uri>http://c3d2.de</uri>
  </author>
  <title>{{title}}</title>
  <id>averyuniqid:D</id>
  <link rel='self' href="/atom" />
  <logo>https://www.c3d2.de/w/images/7/71/Pentamedia.png</logo>
  <rights>cc-by-nc-nd</rights>
  <subtitle>{{title}} Feed of pentamedia-portal</subtitle>
  {% if episodes|d([]) != [] %}<updated>{{episodes[-1].date}}</updated>{% endif %}

  {% for episode in episodes|d([]) %}
  <entry>
  <title>{{ episode.name }}</title>
    <link rel="alternate" href="{{pentamediaportal}}/{{clean_category(episode.category)}}/{{episode.link}}"/>
    <link rel="enclosure" href="http://ftp.c3d2.de/{{episode.category}}/{{episode.filename}}"/>
    <id>{{episode.id}}</id>
    <updated>{{episode.date}}</updated>
    <summary>{{remove_html(episode.short)}}</summary>
    <content>{{remove_html(episode.long)}}</content>
  </entry>
  {% endfor %}
</feed>
