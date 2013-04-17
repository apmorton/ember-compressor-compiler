import re

from nose.tools import assert_equal, assert_not_equal
from nose.tools import assert_true, assert_false

from embercompressorcompiler import EmberPrecompiler as EP


class TestEmberPrecompiler(object):
    def test_init(self):
        ep = EP()

        assert_equal(ep.wrap, 'Ember.Handlebars.template({0})')
        assert_equal(ep.namespace, 'Ember.TEMPLATES')

    def test_init_with_wrap_and_namespace(self):
        namespace = 'ns'
        wrap = 'wrp'
        ep = EP(wrap=wrap, namespace=namespace)

        assert_equal(ep.wrap, wrap)
        assert_equal(ep.namespace, namespace)

    def test_init_disable_wrap_and_namespace(self):
        ep = EP(wrap=False, namespace=False)

        assert_false(ep.wrap)
        assert_false(ep.namespace)

    def test__compile(self):
        source = ""
        ep = EP()

        compiled = ep._compile(source)
        assert_true(compiled.startswith('function'))

    def test__wrap(self):
        source = 'test'
        wrap = 'test_wrap({0})'
        expected = 'test_wrap(test)'
        ep = EP(wrap=wrap)

        wrapped = ep._wrap(source)

        assert_equal(expected, wrapped)

    def test__namespace(self):
        source = 'test'
        namespace = 'TEMPLATES'
        name = 'app_template'
        expected = 'TEMPLATES["app_template"] = test;'
        ep = EP(namespace=namespace)

        wrapped = ep._namespace(name, source)

        assert_equal(expected, wrapped)

    def test_compile_with_wrap_and_namespace(self):
        source = '{{test}}'
        wrap = 'template({0})'
        namespace = 'T'
        name = 't'
        expected_re = r'^T\["t"\] = template\(function .+\);$'
        ep = EP(wrap=wrap, namespace=namespace)

        compiled = ep.compile(name, source)

        matches = re.match(expected_re, compiled, flags=re.DOTALL)

        msg = '{0} doesn\'t match RE {1}'.format(compiled, expected_re)
        assert_not_equal(matches, None, msg)

    def test_compile_disable_wrap_and_namespace(self):
        source = '{{test}}'
        expected_re = r'^function .+}$'
        ep = EP(wrap=False, namespace=False)

        compiled = ep.compile(None, source)

        matches = re.match(expected_re, compiled, flags=re.DOTALL)

        msg = '{0} doesn\'t match RE {1}'.format(compiled, expected_re)
        assert_not_equal(matches, None, msg)
