(function() {
  'use strict';

  angular
    .module('ui')
    .config(config);

  config.$inject = ['$logProvider'];

  function config($logProvider) {
    // Enable log
    $logProvider.debugEnabled(true);
  }

})();
