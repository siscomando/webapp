SisComando
============

The SisComando is the tool to make the orchestration of the problems in 
a critical enviroment of TIC.

Important
=========
All modifications in components (bower_components dir) are tracked in 
their specifics repos, because is not needs put it inner in the webapp's repo.
Furthermore the content of the custom components is placed within of app.html
after ran vulcanize.

Setup App
=========
This app uses [vulcanize]() to reduce loads dependences of the HTML's imports.
The file `build.html` is used to setup all that is needed to work fine this app. 
It contains some elements required and others are built-in inside them. 
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
# when gravatarEnabled=true the avatar attribute must be md5 hash from email.
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
In sc-navbar the returned JSON after GET in `url` attribute must be a list of
objects with the fields:
```
{
  "issues": [
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
In sc-navbar the returned JSON after "GET" in `stream` attribute (or Server Side Event reading resource) must be an object with the fields:
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







