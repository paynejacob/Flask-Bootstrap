(function() {
  'use strict';

  // Third party shims
  angular.module('underscore', []).factory('_', function() { return window._; });
  angular.module('moment', []).factory('moment', function() { return window.moment; });
  angular.module('components', ['underscore', 'moment']); //see vendor/dateTransformer.js

  // Define modules here so that file concatenation ordering doesn't
  // break the app.  This is a poor man's Browserify/RequireJS.
  angular.module('Application.services', [
    'ngResource'
  ]);
  angular.module('Application.controllers', []);
  angular.module('Application', [
    'components',
    'ui.bootstrap',
    'ui.router',
    'flask-assets-templates',
    'Application.services',
    'Application.controllers',
    'toaster'
  ]);

})();
