# API's specifications
#
# Schema
# =====================
# All API access is over HTTP[S] and accessed from the siscomando.example/api/v2/.
# All data is sent and received as JSON.
#
# Date and Time
# =====================
# All timestamps are returned in ISO 8601 format:
# YYYY-MM-DDTHH:MM:SSZ
#
# Parameters
# =====================
# For GET requests, any parameters not specified as a path in the URL can be 
# passed as an HTTP query string parameter:
# $ curl -i "https://siscomando.example/api/v2/issues/supgs?closed=true"
# In this example, the `supgs` is provided for the `Organization Unit while 
# `closed` is passed in the query string.
#
# For POST, PATCH, PUT and DELETE requests parameters not represented in path in
# the URL should be encoded as JSON with "Content-Type of application/json".
# $ curl -i -u username 
#    -d '{"comment": {"body":"This simples message"}}' 
#    https://siscomando.example/api/v2/comments
# 
# Root Endpoint
# =====================
# A GET request to the root endpoint get all the resources that the API supports.
# $ curl https://siscomando.example
#
# Client Errors
# =====================
# 
from siscomando import webservice