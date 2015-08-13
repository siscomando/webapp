/**
 * SisComando Javascript Library v0.1.1
 *
 * Copyright 2015 Siscomando and other contributors
 * Released under the MIT license
 * http://siscomando.github.io/api
 *
 *
 * .. versionchanged:: 0.1.1
 *    Adds helpers to help build urls
 *    Change filter for python filters supported by API (e.g:?where=name==XXX)
 */

var siscomando = siscomando || {};

// RESTApi Settings
siscomando.apiSERVER = "http://localhost:9014"; // YOUR_URL_API_ADDRESS
siscomando.apiPREFIX = "/api/v2"; // YOUR_URL_API_PREFIX. Removes slash from the end.
siscomando.apiURL = siscomando.apiSERVER + siscomando.apiPREFIX;
// Push Notifications Settins: stream for server side events.
siscomando.streamSERVER = "http://notes.local"; // YOUR_URL_API_ADDRESS
siscomando.streamPREFIX = "/v1"; // YOUR_URL_API_PREFIX. Removes slash from the end.
siscomando.streamURL = siscomando.streamSERVER + siscomando.streamPREFIX;

/**
 * This `urls` are based in the documentation Siscomando's API. The goal here is
 * that it to be a constrains and not modified in runtime.
 * See more info in http://siscomando.github.io/api/
 *
 * All urls point to resources scope. The three main are: `comments`, `issues`
 * and `users`. Each pointer have the properties:
 *
 * @property {pattern} string for match with replace. It'll change to itemId.
 * @property {item} url with pattern before change. e.g: /resource/<itemId>
 * @property {resources} url with ? before change. e.g: /resource?
 * @property {create} url to create (POST) item.
 * @property {update} url to update (PATCH) item.
 * @property {delete} url to delete (DELETE) item.
 *
 * ******* NOTE *******
 * Some of this properties can never be used or not implemented or will be implemented
 * in the future. We must to do an introspect before the use to check current
 * implementation.
 *
 */
siscomando.urls = {
  comments: {
    pattern: "COMMENT_ID", // The pattern to replace by ID
    item: "/comments/COMMENT_ID?", // define item url to comments
    resources: "/comments?", // define item url to comments
    // Actions. read is a default action so are directly defined in `item` and
    // `resources`
    create: "/comments/new", // HTTP POST verb
    update: "/comments/edit/COMMENT_ID", // HTTP PATCH verb
    delete: "/comments/edit/COMMENT_ID", // HTTP DELETE verb
    stream: "/comments"
  },
  issues: {
    pattern: "ISSUE_ID", // The pattern to replace by ID
    item: "/issues/ISSUE_ID?", // define item url to issues
    resources: "/issues?", // define item url to issues
    create: "/issues/", // HTTP POST verb
    update: "/issues/", // HTTP PATCH verb
    delete: "/issues/", // HTTP DELETE verb
    stream: "/issues"
  },
  users: {
    pattern: "USER_ID", // The pattern to replace by ID
    item: "/users/USER_ID?", // define item url to users
    resources: "/users?", // define item url to users
    create: "/users", // POST must be used by client.
    update: undefined, // not implemented
    delete: undefined, // not implemented
    stream: undefined // not implemented
  },
  // `me` scope is useful for current actions. Gets /me will return always an item.
  me: {
    pattern: "USER_ID", // The pattern to replace by ID
    item: "/me/",
    resource: "/me/",
    create: undefined, // not implemented
    // This `update` can incoherence but PATCH only is supported for `item_id` or
    // item scope.
    update: "/me/USER_ID",
    delete: undefined, // not implemented
    stream: undefined // not implemented
  },
  stars: {
    pattern: "STAR_ID", // The pattern to replace by ID
    item: "/stars/STAR_ID?", // define item url to users
    resources: "/stars?", // define item url to users
    create: "/stars/new", // POST must be used by client.
    update: undefined, // not implemented
    delete: undefined, // not implemented
    stream: undefined // not implemented
  },
}

/**
 * The RESTApi used for Siscomando defines resources as the point of contact
 * of the client to consume data. When we make reference the word `resource`
 * we are referring to a collection of data. And when we use `item` the referrer
 * is for a specific item of this collection.
 */
siscomando.helpers = {
  // dumps all urls of this API. Samples for developers purposes.
  // Using helpers for this.
  dumpsUrls: function() {

  },
  queries: {
    where: function(url, field, value) {
      url = fixURL(url);
      return url + 'where=' + field + '=="' + value + '"';
    },
    embedded: function(url, fields) {
      isArrary = fields instanceof Array;
      url = fixURL(url);
      if (!isArrary) {
          return url + 'embedded=' + '{' + fields + ':1}';
      }
      if (isArrary) {
        value = {};
        for (idx in fields){
          value[fields[idx]] = 1;
        }
        return url + 'embedded=' + JSON.stringify(value);
      }
    }
  },
  comments: {
    item: {

    },
    resources: {
      /**
       * `getUrl` gets url to get comments from API. This is even that to access
       * `siscomando.urls.comments.resources`, except because embedded fields
       *  are expanded when using this.
       * @returns: list of comments with embedded (author, issue, stars).
       */
      getUrl: function() {
        var manager = siscomando.urls.comments;
        var relativeUrl = manager.resources;
        var absURL = siscomando.apiURL + relativeUrl;
        var fields = ["author", "issues", "stars"];
        return queryString.embedded(absURL, fields);
      },
      /**
       * `getByIssue` gets comments by issue_id (e.g: pk)
       * @param issueId: item_id (e.g: pk)
       * @returns: list of comments with embedded (author, issue, stars).
       */
      getUrlByIssue: function(issueId) {
        var manager = siscomando.urls.comments;
        var relativeUrl = manager.resources;
        var absURL = siscomando.apiURL + relativeUrl;
        var concated = queryString.where(absURL, "issue", issueId);
        var fields = ["author", "issues", "stars"];
        return queryString.embedded(concated, fields);
      },
      getByIssue: function(issueId) {
        // get response from api using XMLHTTPRequest.
        // not implemented.
      },
      /**
       * `getUrlByRegister` gets comments by register number
       * @param registerNumber: string e.g: 2015RI000012311
       * @returns: list of comments with embedded (author, issue, stars).
       */
      getUrlByRegister: function(registerNumber) {
        var manager = siscomando.urls.comments;
        var relativeUrl = manager.resources;
        var absURL = siscomando.apiURL + relativeUrl;
        var concated = queryString.where(absURL, "register", registerNumber);
        var fields = ["author", "issues", "stars"];
        return queryString.embedded(concated, fields);
      },
      getByRegister: function(registerNumber) {
        // get response from api using XMLHTTPRequest.
        // not implemented.
      },
      /**
       * `getUrlToSearch` makes url to search within comments.
       * @param term: string
       * @returns: list of comments filtered by term with embedded (author,
       * issue, stars).
       */
      getUrlToSearch: function(term) {
        var manager = siscomando.urls.comments;
        var relativeUrl = manager.resources;
        var absURL = siscomando.apiURL + relativeUrl;
        var fields = ["author", "issues", "stars"];
        absURL = queryString.embedded(absURL, fields);
        return absURL + '&search=' + term;
      },
      /**
       * `getUrlToCreate` makes url to create new comment.
       * @returns: the url for create comments.
       */
      getUrlToCreate: function() {
        var manager = siscomando.urls.comments;
        var relativeUrl = manager.create;
        var absURL = siscomando.apiURL + relativeUrl;
        return absURL;
      },
    },
    stream: {
      /**
       * `getUrl` gets url for consume comments by stream.
       * @returns: url to connect with channel's stream.
       */
      getUrl: function() {
        var manager = siscomando.urls.comments;
        var relativeUrl = manager.stream;
        var absURL = siscomando.streamURL + relativeUrl;
        return absURL
      },
      /**
       * `getUrlByIssue` gets url for consume comments by stream.
       * @param issueId: item_id (e.g: pk)
       * @returns: url to connect with channel's stream.
       */
      getUrlByIssue: function(issueId) {
        var manager = siscomando.urls.comments;
        var relativeUrl = manager.stream;
        var absURL = siscomando.streamURL + relativeUrl;
        return absURL + '/' + issueId;
      }
    }
  },
  issues: {
    item: {
      /**
       * `getUrl` makes the url to get an issue item.
       * @param issue_or_register: issue_id (e.g: pk) or register
       * @returns: an issue
       */
      getUrl: function (issue_or_register) {
        var manager = siscomando.urls.issues;
        var pattern = manager.pattern;
        var relativeUrl = manager.item;
        relativeUrl = relativeUrl.replace(pattern, issue_or_register);
        var absURL = siscomando.apiURL + relativeUrl;
        return absURL;
      },
      // TODO: encapsulate for this can be used.
      // ROADMAP:v0.1.2
      // getUrlByRegister: this.getUrl, // alias. TODO: encapsulate it.
      // getUrlByIssue: this.getUrl, // alias. TODO: encapsulate it.
    },
    resources: {
      /**
       * `getUrlGrouped` makes url gets issues grouped by title.
       * @returns: list of issues as [{title:'SCCD', issues:[{a}, {b}, {c}]}]
       * where a, b and c are item object.
       */
      getUrlGrouped: function() {
        var manager = siscomando.urls.issues;
        var relativeUrl = manager.resources;
        var absURL = siscomando.apiURL + relativeUrl;
        return absURL + '&grouped=' + 1;
      }
    },
    stream: {
      /**
       * `getUrl` gets url for consume issues by stream.
       * @returns: the url to connect with channel's stream.
       */
      getUrl: function() {
        var manager = siscomando.urls.issues;
        var relativeUrl = manager.stream;
        var absURL = siscomando.streamURL + relativeUrl;
        return absURL
      }
    },
  },
  users: {
    item: "", // define item helpers to users
    resources: {
      /**
       * `getUrlToSearch` makes url to search within users with max_results.
       * @param term: string
       * @returns: list of users filtered by username.
       */
      getUrlToSearch: function(term) {
        var manager = siscomando.urls.users;
        var relativeUrl = manager.resources;
        var absURL = siscomando.apiURL + relativeUrl;
        return absURL + '&search=' + term + '&max_results=5';
      }
    },
  },
  stars: {
    item: {},
    resources: {
      /**
       * `getUrlToCreate` makes url to create new stars.
       * @returns: the url for create stars (voting).
       */
      getUrlToCreate: function() {
        var manager = siscomando.urls.stars;
        var relativeUrl = manager.create;
        var absURL = siscomando.apiURL + relativeUrl;
        return absURL;
      },
    },
    stream: {}
  }
};

siscomando.behaviors = {
  hashLink: {
    exec: function() {
      links = document.querySelectorAll("html /deep/  a.hashLink");
    };
  },
}
/**
 *
 * ALIAS
 *
 * ALL = [queryString, scUrls]
 */

/**
 * Prepares the url to add params (querystrings). This is an alias to
 * siscomando.helpers.queries. The options are `where` and `embedded`.
 *
 *    where(url, field, value)
 *    @param url: the url will be modified
 *    @param field: the field to filter
 *    @param value: the value
 *
 *    embedded(url, fields)
 *    @param url: the url will be modified
 *    @param fields: a string or list of strings with embedded fields.
 */
queryString = siscomando.helpers.queries;
scUrls = siscomando.urls;

/**
* Polyfills and other utilities. Place it to here.
*/

// added `endsWith`
if (!String.prototype.endsWith) {
 String.prototype.endsWith = function(searchString, position) {
     var subjectString = this.toString();
     if (position === undefined || position > subjectString.length) {
       position = subjectString.length;
     }
     position -= searchString.length;
     var lastIndex = subjectString.indexOf(searchString, position);
     return lastIndex !== -1 && lastIndex === position;
 };
}

/**
 * Prepares the url to add params (querystrings)
 */
fixURL = function(url) {
    if (url.endsWith("?")) {
      return url;
    } else {
      if (url.indexOf("?") > -1) {
        if (url.endsWith("&")) {
          return url;
        } else {
          return url + "&"
        }
      } else {
        return url + "?"
      }
    }
}
/** end polyfills area **/

/****************************************************************************
 * Setup URL for all elements. When the urls are dinamic the functions above
 * working as shortcuts.
*****************************************************************************/
var scNavbar = document.querySelector('sc-navbar');
var scSearch = document.querySelector('sc-search');
var scTimeline = document.querySelector('sc-timeline');
var lpInput = document.querySelector('lp-input');

// sc-navbar: left menu. It receives `issues` from GET and SSE
// `url` is to GET; `stream` is to SSE
scNavbar.url = siscomando.helpers.issues.resources.getUrlGrouped();
scNavbar.stream = siscomando.helpers.issues.stream.getUrl();
// sc-timeline: this is the container with feeds of the messages. It consumes
// GET, SSE
scTimeline.url = siscomando.helpers.comments.resources.getUrl();
scTimeline.sseurl = siscomando.helpers.comments.stream.getUrl();
scTimeline.urlrate = siscomando.helpers.stars.resources.getUrlToCreate()
// lp-input: It's used to post comment by POST in `url` or GET internal users
// for mentions.
lpInput.url = siscomando.helpers.comments.resources.getUrlToCreate();
