# Simple Spotify Music Browser

This is a simple django application which consumes the spotify web search api to to display names and images of tracks, albums, artists and playlists.

Software Requirements:
* Python3.4+
* Django

The entire application can be setup with the following steps:
1. create and activate a virtualenv
2. pip install -r requirements.txt
3. python manage.py test (optional)
4. python manager.py runserver
5. open the browser and visit http://localhost:8000

Design:

The main parts of the application can be found in the module called spotify_proxy.

There is a single view called index_view with parses get parameters q and filter, calls the api_wrapper for spotify and renders the html page with the results. I chose to keep the api_wrapper seperately from the view to make the view more easily extensible for future cases when we'd require to expose a json api instead of an HTML page.

The api_wrapper is a simple abstraction over the spotify web api using the python requests library. 
The get_track_list function validates query parameters and then calls the spotify api. It then parses the response json to remove all the unecessary fields and return a list of items and the total count of the query present with spotify.

The result is then rendered as html using a template defined using django's default templating language. The template contains a an html form which sends get requests to the same index url.

I have also included a set of tests in the spotify_proxy app which validates the context of each possible query on the server and ensures that valid responses are retreived.

