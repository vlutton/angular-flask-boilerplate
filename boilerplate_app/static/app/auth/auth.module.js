(function() {
  'use strict';
  angular
    .module('boilerplate.auth', [
      'satellizer',
      'ui.router',
      'ngMessages'
    ]).constant('API', '')
    .config(function($authProvider) {
      $authProvider.loginUrl = '/auth';
      $authProvider.signupUrl = '/users';
    });

})();
