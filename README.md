Ember Compressor Compiler
=========================

[![Build Status](https://travis-ci.org/Juvenal1228/ember-compressor-compiler.png?branch=master)](https://travis-ci.org/Juvenal1228/ember-compressor-compiler)

Purpose
-------

This tool is meant to be used as an extension to [django-compressor](https://github.com/jezdez/django_compressor)

It precompiles [handlebars.js](https://github.com/wycats/handlebars.js) templates specifically for [ember.js](https://github.com/emberjs/ember.js)


Features
--------

- platform independent
- no need to install node.js packages
- flexible template naming conventions
- inline handlebars in django templates
- 100% test coverage
- [PEP 8](http://www.python.org/dev/peps/pep-0008/) compliance
- [semver](http://semver.org/) compliance


Installing
----------

Install with pip/easy_install from the pypi

`pip install ember-compressor-compiler`

or clone the latest source

    git clone https://github.com/Juvenal1228/ember-compressor-compiler.git
    cd ember-compressor-compiler
    python setup.py install

You must also install [node.js](http://nodejs.org/) or [PyV8](https://code.google.com/p/pyv8/)

The latest versions of node.js can be found [here](http://nodejs.org/download/)

Using
-----

Using this tool is as simple as installing it and adding it to the `COMPRESS_PRECOMPILERS` django setting

```python
COMPRESS_PRECOMPILERS = (
    ('text/x-handlebars', 'embercompressorcompiler.filter.EmberHandlebarsCompiler'),
)
```

Then, in your django templates you can embed handlebars templates like so
```html+django
{% load staticfiles %}
{% load compress %}

{% compress js %}
<script type="text/x-handlebars" src="{% static 'app/templates/application.hbs' %}" ></script>
<script type="text/x-handlebars" data-template-name="index">
    {{outlet}}
</script>
{% endcompress %}
```

Template Names
--------------

Template names are determined in one of two ways

1. the `data-template-name` attribute on the `script` tag in your django template
2. the `src` attribute on the `script` tag in your django template

When specified, the `data-template-name` value is used verbatim

If not, the `src` value is manipulated to give proper template names.

- the file extensions `.handlebars` and `.hbs` are removed
- everything before the parent directory `templates` is removed


```html+django
<!-- results in template named 'application' -->
<script type="text/x-handlebars" src="{% static 'app/templates/application.hbs' %}" ></script>

<!-- results in template named 'example/index' -->
<script type="text/x-handlebars" src="{% static 'app/templates/example/index.handlebars' %}" ></script>
```

Advanced Usage
--------------

If you need to change the template naming behavior, you can subclass `embercompressorcompiler.filter.EmberHandlebarsCompiler`

```python
from embercompressorcompiler.filter import EmberHandlebarsCompiler

class MyCompiler(EmberHandlebarsCompiler):
    # override default parent directory
    parent_dir = 'tpls'
    
    # override default extensions
    extensions = ['.tpl']
```

Then you register your own compiler subclass in `COMPRESS_PRECOMPILERS`

```python
COMPRESS_PRECOMPILERS = (
    ('text/x-handlebars', 'myapp.MyCompiler'),
)
```
