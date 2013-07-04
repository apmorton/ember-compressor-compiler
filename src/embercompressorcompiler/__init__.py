import execjs
from pkg_resources import resource_string


class EmberPrecompiler(object):
    def __init__(self, wrap=None, namespace=None):
        if wrap is None:
            wrap = 'Ember.Handlebars.template({0})'
        if namespace is None:
            namespace = 'Ember.TEMPLATES'
        self.wrap = wrap
        self.namespace = namespace
        self.__setup()

    def __setup(self):
        source = ''
        for js in ['compiler', 'handlebars', 'ember-template-compiler']:
            source += resource_string(__name__, 'js/{0}.js'.format(js))
        self.ctx = execjs.compile(source)

    def _compile(self, source):
        return self.ctx.call('precompile', source)

    def _wrap(self, compiled):
        return self.wrap.format(compiled)

    def _namespace(self, name, compiled):
        return '{0}["{1}"] = {2};'.format(self.namespace, name, compiled)

    def compile(self, name, source):
        compiled = self._compile(source)

        if self.wrap:
            compiled = self._wrap(compiled)

        if self.namespace:
            compiled = self._namespace(name, compiled)

        return compiled
