Simple cherrypy server app for consuming and displaying JSON posted data
------------------------------------------------------------------------

It is a demonstration of consuming data that is posted as json or xml from the webhook restservice in [Onadata](https://github.com/onaio/onadata).

For the submitted JSON data if it has the key `_id` key, it will be stored in an in-memory database with [TinyDB](https://github.com/msiemens/tinydb) that stores at most 10 records.

Running it
----------

```
$ pip install -r requirements.txt
$ python controller.py
```

Examples
--------

if you post a json file, you should get as response `{"status": "OK"}`

```
$ curl -d @json_data.json localhost:8080 -H "Content-Type:application/json"
{"status": "OK"}

```


Docker
------

Run It

```
$ docker run --name consumer --rm -d -p 8080:8080 ukanga/data-post-consumer
```

View Logs

```
$ docker logs -f consumer
```

Stop It

```
$ docker stop consumer
```

Rebuild It

```
$ docker build -t ukanga/data-post-consumer
```
