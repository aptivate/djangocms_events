# DjangoCMS Events

Django-CMS Events app.

[![Build Status on Travis](https://travis-ci.org/aptivate/djangocms_events.svg?branch=master)](https://travis-ci.org/aptivate/djangocms_events)

## Purpose

A customisable Events app where you can choose your own Model with the
DJANGOCMS_EVENTS_MODEL setting.

## Contents

The Github project contains the following files and directories:

* djangocms_events: the app which you can add to `INSTALLED_APPS` in Django.
  * templates: the supplied templates, with reusable fragments.
  * cms_app.py: A full page application for listing and searching for events.
  * cms_plugins.py: A plugin to put in sidebars for listing smaller numbers of events.
  * conf.py: Processes the DJANGOCMS_EVENTS_MODEL setting.
  * feeds.py: Generates RSS feeds for events.
  * forms.py: Event search form.
  * menu.py: The sidebar for the full page CMS app.
  * models.py: An empty models file to keep Django happy.
  * urls.py: URLs for the full page CMS app, search and feed.
  * views.py: Event detail, list and search views.

* tests: A test project which includes the Events app, some models and tests.
  * events: Is the customisation of the Events CMS app;
    * admin.py: Example admim customisation for event model.
    * models.py: Example of model that could be used for your own events.
    * search_indexes.py: Example haystack indexes for the above model.
    * templates/search/indexes/events/event_text.txt: The template for indexing the above event model.

## Usage

### With DYE

To add `djangocms_events` to your DYE project:

* add this line to `deploy/pip_packages.txt`:
    -e git+https://github.com/aptivate/djangocms_events.git
* run `deploy/bootstrap.py`

### Manual Installation

If you're not using DYE, then install `djangocms_events` in your global Python
environment or virtualenv:

    pip install djangocms_events

Or if it's not available on PyPI, or you need a newer version:

    pip install -e git+https://github.com/aptivate/djangocms_events.git

Of course you need [Django](https://www.djangoproject.com/)
(1.5 or higher) and
[Django-CMS](https://www.django-cms.org/en/) (2.4 or higher) in your
environment as well. They'll be installed automatically by Pip if you don't
have them already.

### Creating a Model

You need a model to use with your events. Because events can differ so much,
no standard model is provided, but you can use the one from our tests as a
starting point, and customise it to meet your needs.

Create an app in your project, for example called `events` (or whatever you
like) and add a model in `models.py` similar to the one you'll find in
this project's GitHub. **todo include the URL**

### Add to `INSTALLED_APPS`

Add `djangocms_events` to `INSTALLED_APPS` in your project's `settings.py` file:

    INSTALLED_APPS = (
        ...
        'djangocms_events',
    )

Also add a line that sets DJANGOCMS_EVENTS_MODEL to point to the model that
you created earlier:

    DJANGOCMS_EVENTS_MODEL = 'events.models.MyEvent'

### Installing the Views

To provide access to the included views, you have two options:

You can create a Django-CMS page and attach the "Events App" to it.
All URLs will be relative to this page's URL (slug), which can be translated
into different languages (e.g. `/en/search` and `/es/buscar`).
You can find the *Application* setting under *Advanced Settings* when
editing the page. Remember to restart the webserver after you do this,
because Django-CMS caches the URL mapping for CMS Apps at server startup.

Alternatively, you can modify your global URL mapping to include the
Events App views directly, by adding the following lines to `urls.py` in
your project root:

    import django.contrib.auth.urls
    import djangocms_events
    urlpatterns += patterns('', url('', include(djangocms_events.urls)))

### Running the tests

You can clone the project from GitHub and run the tests manually with the
`tox` command, which installs all the test dependencies for you:

    tox

This will test with Python 2.6 and 2.7, so you'll need both installed. If
you just want to test one environment (which is faster and doesn't require
two Pythons to be installed) you can do this:

    tox -e py27-django16-cms3

## Customisation

### Resuing the templates

The templates included with djangocms_events can be reused by:

Making a copy of the parent files 'djangocms_events/tempaltes/events/Copy one of the 

### Template reuse in Django

In Django you can reuse templates by:

* overriding a template file, by placing a file with the same name and path
  in the `templates` directory of one of your own apps.
* extending a template file, by creating a file with a *different* name that
  starts with `{% extends "basetemplate.html" %}`.

### Parent templates

The supplied templates in `djangocms_events` inherit from a file called
`base.html` which may not exist in your project. You can create one which
extends your own base template, whatever that's called, for example:

    {% extends "myapp/root.html" %}

    {% block my_content_middle %}
        {% block main %}
            The DjangoCMS-Events HTML will be inserted here
        {% endblock %}
    {% endblock %}

Or you can create a directory called `events` under `templates` in one of
your apps, copy one or more template files from `djangocms_events` into that
directory and modify them. Provided your app appears **before**
`djangocms_events` in your INSTALLED_APPS list, your template will override
(replace) the one supplied in `djangocms_events`.

The views directly use the following templates:

* event_detail.html: detail page for a single event
* event_list.html: the full page CMS App uses this template
* event_summary_plugin.html: template used by the Event Summary List plugin
  (gives the event title only)
* event_detail_plugin.html: template used by the Event Detail List plugin
  (gives more detail about each event)
* search.html: the full page CMS App uses this for the search page, to
  show the search form and results list.

These templates in turn include some fragments for repeated or reused
blocks of HTML code:

* event_detail_fragment.html
* event_detail_main_fragment.html
* event_list_fragment.html
* search_fragment.html
