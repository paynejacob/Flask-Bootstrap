# -*- coding: utf-8 -*-
""" Define our asset bundles for front-end minification """
from flask_webpack import Webpack

webpack = Webpack()

__all__ = ["webpack"]
# vendor_css = Bundle(
#   "libs/bootswatch-dist/css/bootstrap.min.css",
#   "libs/angularjs-toaster/toaster.min.css",
#   filters="cssmin",
#   output="css/vendor.min.css"
# )

# app_css = Bundle(
#   "css/style.scss",
#   filters=["pyscss", "cssmin"],
#   output="css/app.min.css"
# )

# vendor_js = Bundle(
#   "libs/jquery/dist/jquery.js",
#   "libs/bootstrap/dist/js/bootstrap.min.js",
#   "libs/angular/angular.min.js",
#   "libs/angular-bootstrap/ui-bootstrap-tpls.min.js",
#   "libs/angular-ui-router/release/angular-ui-router.min.js",
#   "libs/angular-resource/angular-resource.min.js",
#   "libs/angular-animate/angular-animate.min.js",
#   "libs/lodash/lodash.min.js",
#   "libs/moment/min/moment.min.js",
#   "libs/angularjs-toaster/toaster.min.js",
#   filters='jsmin',
#   output="js/vendor.min.js"
# )

# app_js = Bundle(
#   "js/modules.js", # modules.js must be first!
#   "js/Application.js",
#   "js/services.js",
#   "js/controllers/*.js",
#   "js/vendor/*.js",
#   filters="jsmin",
#   output="js/app.min.js"
# )

# angular_templates_js = Bundle(
#   "partials/*.html",
#   "partials/widgets/*.html",
#   filters=AngularTemplateCacheFilter,
#   output="js/partials.min.js"
# )

# assets = Environment()

# assets.register("app_js", app_js)
# assets.register("vendor_js", vendor_js)
# assets.register("angular_templates_js", angular_templates_js)
# assets.register("app_css", app_css)
# assets.register("vendor_css", vendor_css)
