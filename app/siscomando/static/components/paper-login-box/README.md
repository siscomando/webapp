paper-login-box
================

## Getting Started

Download the element using bower. For that, enter

    bower install --save paper-login-box

And the element will be installed and persisted in your bower.json.


## Using the element
Usage is very simple. Just type

```html
<paper-login-box></paper-login-box>
```

and you're good to go!

The element only fires its `paper-login-box-click` event, if both
the identification value and password value are filled. In the event detail,
there is a field `identifier` and a field `password`, both should be quite self-
explanatory.
