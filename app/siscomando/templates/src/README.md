src folder
================

This folder contains the templates that will to be vulcanized. This folder is
the work place of the developer Polymer. Vulcanize reduce an HTML file and its
dependent HTML Imports into one file.


[Vulcanize Repo](https://github.com/polymer/vulcanize). See more...

Sample command
--------------
vulcanize -o ../login.html login.html -p /Users/horacioibrahim/Developer/projetos/siscomando/app/siscomando

```
Web pages that use multiple HTML Imports to load dependencies may end up making
lots of network round-trips. In many cases, this can lead to long initial load
times and unnecessary bandwidth usage. The Vulcanize tool follows HTML Imports
and <script> tags to inline these external assets into a single page, to be used
 in production.

In the future, technologies such as HTTP/2 and Server Push will likely obsolete
the need for a tool like vulcanize for production uses.
```
