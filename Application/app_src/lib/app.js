module.exports = {
  message: "hello world"
}

console.log("goooodie")
// (function() {
//   'use strict';

//   angular
//     .module('Application')
//     .config(AppConfig)
//     .run(AppRun);

//   AppConfig.$inject = ['$stateProvider', '$urlRouterProvider', '$resourceProvider'];

//   function AppConfig($stateProvider, $urlRouterProvider, $resourceProvider) {
//     $urlRouterProvider.otherwise("/");

//     // Normal analyst states
//     $stateProvider
//       .state('dashboard', {
//         url: '/',
//         templateUrl: '/static/partials/dashboard.html',
//       });

//     // Don't strip trailing slashes from calculated URLs
//     $resourceProvider.defaults.stripTrailingSlashes = false;

//   }

//   AppRun.$inject = ['$rootScope'];

//   function AppRun($rootScope) {
//     // Expose `_.` methods in any template
//     $rootScope._ = _;

//     $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
//       // Scroll to top of page on any state change.
//       // This is coupled with the `autoscroll="false"` on the ui-view tag
//       // in Application/templates/dashboard.html
//       $('html, body').animate({scrollTop: 0}, 200);

//     });
//   }
// })();
