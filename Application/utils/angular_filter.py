# -*- coding: utf-8 -*-
import json, os
from flask_assets import Filter, register_filter


class AngularTemplateCacheFilter(Filter):
    """ A Flask-Assets filter for compressing AngularJS templates and storing
        them in the $templateCache to improve application performance.
    """

    angular_module = 'flask-assets-templates'
    name = 'angulartemplatecache'

    template_start = "angular.module('%s', []).run(['$templateCache', function($templateCache) {\n"
    template_file  = "  $templateCache.put('{rel_path}', {escaped_html});\n"
    template_end   = "}]);\n"

    def input(self, _in, out, source_path=None, **kwargs):
        """ prepare each file before concatenating """
        #base_path = os.path.dirname(source_path)
        rel_path = source_path[source_path.index('/static/partials'):]
        html_template = _in.read()
        out.write(self.template_file.format(rel_path=rel_path, escaped_html=json.dumps(html_template)))

    def output(self, _in, out, output_path=None, **kwargs):
        """ after concatenating, just throw it back out """
        out.write(self.template_start  % (self.angular_module)) #js brace breaks .format
        out.write(_in.read())
        out.write(self.template_end)


register_filter(AngularTemplateCacheFilter)
