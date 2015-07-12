(function() {
'use strict';

angular
  .module('Application.controllers')
  .controller('FlaskToasterCtrl', FlaskToasterCtrl);

FlaskToasterCtrl.$inject = ['$scope', 'toaster', '$rootScope'];

function FlaskToasterCtrl( $scope, toaster, $rootScope) {
  var self = this;
  var allMessages = [];
  var allCategories = [];

  $('.flask-message').each(function(i, obj) {
    allMessages.push(obj.innerHTML)
  });

  $('.flask-category').each(function(i, obj) {
    allCategories.push(obj.innerHTML)
  });

  for (var i in allMessages) {
    toaster.pop(allCategories[i], allMessages[i]);
  }

}

})();
