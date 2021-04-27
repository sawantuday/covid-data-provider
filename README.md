# Covid-19 Twitter data collection service    
A quick Python Flask microservice to parse twitter data and extract availability or requirement of medical services. The main parser is located under [server/services/tweetService.py](https://github.com/sawantuday/covid-data-provider/blob/main/server/services/tweetService.py "tweetService.py"). 

Couple APIs exposed right now are 
1. `GET /api/tweet-data?end=50` - Returns latest 50 tweets in parsed JSON format 
2. `POST /api/parse-text -d {'text': 'text_content'}` - Parse random text data and try to extract medical service list of it, returns JSON. 

All boilerplate code is taken from [IBM Cloud](https://cloud.ibm.com) repository at  [Python Flask](https://github.com/IBM/python-flask-app)   
    
## Steps

### Building locally

To get started building this application locally, you can either run the application natively or use containerized setup for your Python environment.

#### Native application development

* Install [Python](https://www.python.org/downloads/)

Running Flask applications has been simplified with a `manage.py` file to avoid dealing with configuring environment variables to run your app. From your project root, you can download the project dependencies with (NOTE: If you don't have pipenv installed, execute: `pip install pipenv`):


```bash

pipenv install

```

Then, activate this app's virtualenv:

```bash

pipenv shell

```


To run your application locally, run this inside the virtualenv:

```bash

python manage.py start

```

  

`manage.py` offers a variety of different run commands to match the proper situation:

*  `start`: starts a server in a production setting using `gunicorn`.

*  `run`: starts a native Flask development server. This includes backend reloading upon file saves and the Werkzeug stack-trace debugger for diagnosing runtime failures in-browser.

*  `livereload`: starts a development server via the `livereload` package. This includes backend reloading as well as dynamic frontend browser reloading. The Werkzeug stack-trace debugger will be disabled, so this is only recommended when working on frontend development.

*  `debug`: starts a native Flask development server, but with the native reloader/tracer disabled. This leaves the debug port exposed to be attached to an IDE (such as PyCharm's `Attach to Local Process`).

  

There are also a few utility commands:

*  `build`: compiles `.py` files within the project directory into `.pyc` files

*  `test`: runs all unit tests inside of the project's `test` directory

  

Your application is running at: `http://localhost:3000/` in your browser.

- Your [Swagger UI](http://swagger.io/swagger-ui/) is running on: `/explorer`

- Your Swagger definition is running on: `/swagger/api`

- Health endpoint: `/health`

  

There are two different options for debugging a Flask project:

1. Run `python manage.py runserver` to start a native Flask development server. This comes with the Werkzeug stack-trace debugger, which will present runtime failure stack-traces in-browser with the ability to inspect objects at any point in the trace. For more information, see [Werkzeug documentation](http://werkzeug.pocoo.org/).

2. Run `python manage.py debug` to run a Flask development server with debug exposed, but the native debugger/reloader turned off. This grants access for an IDE to attach itself to the process (i.e. in PyCharm, use `Run` -> `Attach to Local Process`).

  

You can also verify the state of your locally running application using the Selenium UI test script included in the `scripts` directory.

  

>  **Note for Windows users:**  `gunicorn` is not supported on Windows. You may start the server with `python manage.py run` on your local machine or build and start the Dockerfile.

  

## License

  

This sample application is licensed under the Apache License, Version 2. Separate third-party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

  

[Apache License FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)