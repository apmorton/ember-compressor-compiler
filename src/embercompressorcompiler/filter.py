from compressor.filters import FilterBase, FilterError
from embercompressorcompiler import EmberPrecompiler


class EmberHandlebarsCompiler(FilterBase):
    """EmberHandlebarsCompiler

    wrap: if specified use as wrapper
        false to disable wrapping

    namespace: if specified use as namespace
        false to disable namespacing
    """

    wrap = None
    namespace = None
    parent_dir = 'templates'
    extensions = ['.hbs', '.handlebars']

    def __init__(self, content, attrs, **kwargs):
        super(EmberHandlebarsCompiler, self).__init__(content, **kwargs)
        self.ep = EmberPrecompiler(wrap=self.wrap, namespace=self.namespace)
        self.attrs = attrs

    def strip_extensions(self, basename):
        for ext in self.extensions:
            if basename.endswith(ext):
                return basename[:-len(ext)]
        return basename

    def strip_parent_dir(self, basename):
        basename = basename.lstrip('/')
        segments = basename.split('/')

        for segment in segments:
            if segment == self.parent_dir:
                idx = segments.index(segment)
                return '/'.join(segments[idx+1:])

        return basename

    def name_from_basename(self, basename):
        basename = self.strip_parent_dir(basename)
        basename = self.strip_extensions(basename)
        return basename

    def determine_name(self, **kwargs):
        name = self.attrs.get('data-template-name', None)

        if not name and 'basename' in kwargs:
            name = self.name_from_basename(kwargs['basename'])

        if not name:
            raise FilterError('template name could not be determined')

        return name

    def input(self, **kwargs):
        name = self.determine_name(**kwargs)
        return self.ep.compile(name, self.content)
