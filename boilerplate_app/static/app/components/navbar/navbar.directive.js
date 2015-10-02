(function() {
  'use strict';

  angular
    .module('ui')
    .directive('boilerplateNavbar', boilerplateNavbar);

  /** @ngInject */
  function boilerplateNavbar() {
    var directive = {
      restrict: 'E',
      templateUrl: 'static/app/components/navbar/navbar.html',
      controller: NavbarController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    NavbarController.$inject = ['$auth', 'AuthService', '$rootScope'];
    function NavbarController($auth, AuthService, $rootScope) {
      var vm = this;

      vm.isAuthenticated = function() {
        return $rootScope.authenticated;
      }
    }
  }

})();
