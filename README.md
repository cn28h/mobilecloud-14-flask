mobilecloud-14-flask
====================

This repo contains versions of the course examples meant to be run with
[Flask](http://flask.pocoo.org/). The examples are divided by week. In each
case, the "main" app file is `app.py`.

Running the Examples
====================

First, install the prequisites. This is most easily done using
[virtualenv](http://virtualenv.readthedocs.org/en/latest/) or with python3
the venv module.  The examples I'll show here are for `virtualenv`.

Create the environment and activate:

```
$ virtualenv env
$ . env/bin/activate
```

Then install from the `requirements.txt` file:

```
(env) $ pip install -r requirements.txt
```

Then, to execute a particular app:

```
(env) $ python app.py runserver
```
