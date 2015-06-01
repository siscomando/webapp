SisComando
============

The SisComando is the tool to help in the communication between teams in the 
process of orchestration of the problems in a critical enviroment of TIC.

Important
=========
All modifications in components (placed bower_components dir) are tracked in 
their specifics repos, e.g: [sc-sse](https://github.com/siscomando/sc-sse), [sc-navbar](https://github.com/siscomando/sc-navbar), etc. because is not needs put each of them within webapp's repo.
Furthermore the content of the custom components will be concatenated within of 
app.html after ran [vulcanize](https://www.polymer-project.org/0.5/articles/concatenating-web-components.html).

Setup App
=========
This app uses [vulcanize](https://github.com/polymer/vulcanize) to reduce loads dependences of the HTML's imports.
The file `build.html` is used to setup all that is needed to work fine this app. 
The app contains some elements required in first level and others are built-in inside them. 
- [sc-navbar](https://github.com/siscomando/sc-navbar): left navigator bar
- [sc-search](https://github.com/siscomando/sc-search): top header bar with search feature
- [sc-timeline](https://github.com/siscomando/sc-timeline): the element that provides our timeline
- [lp-input](http://horacioibrahim.github.io/lp-input/): a fake input/textarea that supports mentions, hashtags on an ordinary
div.

Setup by custom elements
========================
We use [Flask](http://flask.pocoo.org/docs/0.10/) to generate the backend. 
It uses [Jinja2](http://jinja.pocoo.org/) as a full featured template engine for Python.
Note: that our variables is loaded in template using `%% variable %%`. See sample
below:

# sc-navbar attributes
----------------------

```
# when gravatarEnabled=true the <<avatar>> attribute must be md5 hash from email.
    <sc-navbar 
	  username="%% g.user.shortname %%"
	  avatar="%% g.user.md5_email %%"
	  gravatarEnabled="true"
	  online="%% g.user.status_online %%" // boolean
	  url="http://hostname/api/v1/issues" // this returns tickets in JSON format
	  stream="http://hostname/api/v1/stream/issues/" // this returns news tickets 
	  channel="message" // the Server Side Event channel from published messages
     >
    <sc-navbar>
```
In sc-navbar the returned JSON after GET from `url` attribute must be a list of
objects with the fields:
```
{
  "issues": [ // An object <<issues>> containing a list of objects...
    {
      "_cls": "Issue", 
      "_id": {
        "$oid": "555de85ef2c382152fdccc16"
      }, 
      "body": "Problema na conex\u00e3o de... ", 
      "classifier": 0, 
      "created_at": {
        "$date": 1432206894681
      }, 
      "deadline": 120, 
      "register": "2015RI00005742", 
      "register_orig": "2015RI/00005742", 
      "slug": "siorg (sunmp)-2015RI00005742", 
      "title": "SIORG (SUNMP)", 
      "ugat": "SUNFJ", 
      "ugser": "SUPDE"
    }
  ]
}	
```
In sc-navbar the returned JSON after "GET" from `stream` attribute (or Server 
Side Event reading resource) must be an object with the fields:
```
    {
      "_cls": "Issue", 
      "_id": {
        "$oid": "555de85ef2c382152fdccc16"
      }, 
      "body": "Problema na conex\u00e3o de... ", 
      "classifier": 0, 
      "created_at": {
        "$date": 1432206894681
      }, 
      "deadline": 120, 
      "register": "2015RI00005742", 
      "register_orig": "2015RI/00005742", 
      "slug": "siorg (sunmp)-2015RI00005742", 
      "title": "SIORG (SUNMP)", 
      "ugat": "SUNFJ", 
      "ugser": "SUPDE"
    }
```
# sc-search attributes
----------------------
This features isn't implemented.

```
    <sc-search>
    <sc-search>
```
# sc-timeline attributes
----------------------
The `url` and `sseurl` are main attributes that must be changed to your enviroment.

```
# when gravatarEnabled=true the avatar attribute can be image but is required 
# to exist property md5_email. For more:
# https://github.com/siscomando/sc-timeline/blob/master/sc-timeline.html#L49

    <sc-timeline
	  url="http://hostname/api/v1/comments/" // url to GET data
      sseurl="http://hostname/api/v1/stream/comments/" // url to read SSE.
      gravatarEnabled="true"
    >
    <sc-timeline>
```
In sc-timeline the returned JSON after "GET" from `url` attribute must be a list 
of objects containing the fields:
```
{
  "comments": [ // An object <<comments>> containing a list of objects...
    {
      "_id": {
        "$oid": "5567946df2c38227342abf69"
      }, 
      "author": {
        "User": {
          "avatar": null, 
          "location": null, 
          "md5_email": "34a18f0f342919c1bfbeb12de1b74a4f", 
          "shortname": "joilsonmarques", 
          "status_online": true
        }
      }, 
      "body": "Prefiro\u00a0escolher\u00a0pessoas.\u00a0@mariolago\u00a0", 
      "created_at": {
        "$date": 1432840765175
      }, 
      "created_at_human": "19h19 28/5/2015", 
      "hashtags": [
        "#Entrada"
      ], 
      "origin": 0, 
      "shottime": "19h", 
      "stars": 0, 
      "title": "#Entrada"
    }
 ]
}
```
In sc-timeline the returned JSON after "READ" SSE payload from `default` channel 
assigned by `sseurl` attribute must be a object containing the fields:
```
'{"_id": {"$oid": "5567946df2c38227342abf69"}, "created_at": {"$date": 1432840765175}, "shottime": "19h", "body": "Prefiro\\u00a0escolher\\u00a0pessoas.\\u00a0@mariolago\\u00a0como\\u00a0sempre\\u00a0podemos\\u00a0melhorar\\u00a0esse\\u00a0inout\\u00a0#Entrada", "author": {"User": {"status_online": true, "md5_email": "34a18f0f342919c1bfbeb12de1b74a4f", "shortname": "joilsonmarques", "location": null, "avatar": null}}, "stars": 0, "origin": 0, "hashtags": ["#Entrada"], "title": "#Entrada", "created_at_human": "19h19 28/5/2015"}'
```
# lp-input attributes
----------------------
The `mentionsURL` and `url` are main attributes that must be changed to your enviroment.

```
 	<lp-input 
 	  target="editable" // div element with contentEditable="true"
 	  boxTarget="editableRect" // element where mentions and hashtags dialog will be aligned
      mentionsURL="http://localhost:9003/api/v1/users/" // url to search users public data
      url="http://localhost:9003/api/v1/comments/" // url to post comments
      method="POST">
    </lp-input> 
```
The data returned by mentionsURL must be a list with objects containg the fields:

```
{
  "Users": [
    {
      "_id": {
        "$oid": "5554e764f2c382312595cb80"
      }, 
      "created_at": {
        "$date": 1431616820244
      }, 
      "email": "horacioibrahim7707@gmail.com", 
      "md5_email": "9416bb0ba549d98398d8923809986882", 
      "password": null, 
      "shortname": "horacioibrahim7707", 
      "status_online": true
    }
  ]
}
```
The POST's data dispatched by url attribute is:
```
			body: content of the message
			register: ticket to associate comment at issue
			author: the pk from user logged
```
Your backend must contain a view to handling this data.

Next steps: vulcanize the build.html file
===========================================






