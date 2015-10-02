(function() {
  'use strict';

  angular
    .module('ui', [
      'ngAnimate',
      'ngCookies',
      'ngTouch',
      'ngSanitize',
      'restangular',
      'satellizer',
      'ui.router',
      'ui.bootstrap',
      'boilerplate.auth',
      'boilerplate.protected'
    ]);

})();
