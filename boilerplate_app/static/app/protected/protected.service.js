(function() {
  'use strict';

  angular
      .module('boilerplate.protected')
      .factory('ProtectedService', ProtectedService);

  ProtectedService.$inject = ['Restangular', '$q'];
  
  function ProtectedService(Restangular, $q) {
      var Protected = {
        ProtectedDataHandler: Restangular.all('protected_data'),
        getAllProtectedData: getAllProtectedData,
        getSingleProtectedData: getSingleProtectedData,
        addProtectedData: addProtectedData,
        updateProtectedData: updateProtectedData,
        deleteProtectedData: deleteProtectedData
      };

      return Protected;

      function getAllProtectedData() {
        var deferred = $q.defer();
        Protected.ProtectedDataHandler.getList().then(function(data) {
          deferred.resolve(data);
        }, function(error) {
          deferred.reject(error);
        });
        return deferred.promise;
      }

      function getSingleProtectedData(id) {
       var deferred = $q.defer();
        Restangular.one('protected_data', id).get().then(function(data) {
          deferred.resolve(data);
        }, function(error) {
          deferred.reject(error);
        });
        return deferred.promise;
      }

      function addProtectedData(data) {
        var deferred = $q.defer();
        Protected.ProtectedDataHandler.post(data).then(function(data) {
          deferred.resolve(data);
        }, function(error) {
          deferred.reject(error);
        });
        return deferred.promise;
      }

      function updateProtectedData(id, data) {
        var deferred = $q.defer();
        var resource = Protected.getSingleProtectedData(data.id);
        resource.name = data.name;
        resource.description = data.description;
        resource.put(data).then(function(data) {
          deferred.resolve(data);
        }, function(error) {
          deferred.reject(error);
        });
        return deferred.promise;
      }

      function deleteProtectedData(id, data) {
        var deferred = $q.defer();
        Protected.ProtectedDataHandler.put(data).then(function(data) {
          deferred.resolve(data);
        }, function(error) {
          deferred.reject(error);
        });
        return deferred.promise;
      }

  }
})();
