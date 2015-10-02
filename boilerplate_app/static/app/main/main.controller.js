(function() {
  'use strict';

  angular
    .module('ui')
    .controller('MainController', MainController);

  MainController.$inject = ['$timeout'];
  function MainController($timeout) {
    var vm = this;

    vm.classAnimation = '';

    activate();

    function activate() {
      $timeout(function() {
        vm.classAnimation = 'rubberBand';
      }, 4000);
    }
  }
})();
