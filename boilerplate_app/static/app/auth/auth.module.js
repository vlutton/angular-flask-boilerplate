(function() {
  'use strict';
  angular
    .module('boilerplate.auth', [
      'satellizer',
      'ui.router',
      'ngMessages'
    ]).constant('API', 'http://localhost:5000')
    .config(function($authProvider) {
      $authProvider.baseUrl = 'http://localhost:5000';
      $authProvider.loginUrl = '/auth';
      $authProvider.signupUrl = '/users';
    });

})();
