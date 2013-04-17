import re
from nose.tools import assert_equal, assert_not_equal, raises

from django.conf import settings
settings.configure(STATIC_URL='/static/')

from compressor.filters import FilterError
from embercompressorcompiler.filter import EmberHandlebarsCompiler as EHC


class TestEmberHandlebarsCompiler(object):
    def test_strip_extension(self):
        ehc = EHC(None, None)
        test_pairs = {
            'test.hbs': 'test',
            'test.handlebars': 'test',
            'test.bleh': 'test.bleh'
        }

        for basename, expected in test_pairs.iteritems():
            calculated = ehc.strip_extensions(basename)
            assert_equal(expected, calculated)

    def test_strip_parent_dir(self):
        ehc = EHC(None, None)
        test_pairs = {
            '/templates/test1.handlebars': 'test1.handlebars',
            '/templates/nested/test2.hbs': 'nested/test2.hbs',
            '/bleh/blarg/test3.hbs': 'bleh/blarg/test3.hbs',
            '/templates/templates/test4.hbs': 'templates/test4.hbs'
        }

        for basename, expected in test_pairs.iteritems():
            calculated = ehc.strip_parent_dir(basename)
            assert_equal(expected, calculated)

    def test_name_from_basename(self):
        ehc = EHC(None, None)
        ehc.parent_dir = 'tpls'
        ehc.extensions = ['.tpl']
        test_pairs = {
            'app/tpls/application.tpl': 'application',
            'app/tpls/nested/index.tpl': 'nested/index',
            '/tpl/bleh.blarg.tpl': 'tpl/bleh.blarg'
        }

        for basename, expected in test_pairs.iteritems():
            calculated = ehc.name_from_basename(basename)
            assert_equal(expected, calculated)

    @raises(FilterError)
    def test_determine_name_no_name(self):
        ehc = EHC("", {})
        ehc.input()

    def test_determine_name_attr_name(self):
        expected = 'template/name'
        ehc = EHC("", {'data-template-name': expected})

        computed = ehc.determine_name()

        assert_equal(expected, computed)

    def test_determine_name_basename(self):
        basename = 'templates/tplname.hbs'
        expected = 'tplname'
        ehc = EHC("", {})

        computed = ehc.determine_name(basename=basename)

        assert_equal(expected, computed)

    def test_determine_name_both(self):
        basename = 'wrong/template'
        expected = 'template/name'
        ehc = EHC("", {'data-template-name': expected})

        computed = ehc.determine_name(basename=basename)

        assert_equal(expected, computed)

    def test_input(self):
        expected_re = r'^function .+}$'
        ehc = EHC("{{test}}", {'data-template-name': 't'})
        ehc.ep.wrap = False
        ehc.ep.namespace = False

        compiled = ehc.input()

        matches = re.match(expected_re, compiled, flags=re.DOTALL)

        msg = '{0} doesn\'t match RE {1}'.format(compiled, expected_re)
        assert_not_equal(matches, None, msg)
