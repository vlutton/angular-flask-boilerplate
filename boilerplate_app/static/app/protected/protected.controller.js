(function() {
  'use strict';

  angular
      .module('boilerplate.protected')
      .controller('ProtectedController', ProtectedController);

  ProtectedController.$inject = ['ProtectedService', 'Restangular', '$modal'];

  function ProtectedController(ProtectedService, Restangular, $modal) {
      var vm = this;

      vm.protectedData = null;
      vm.noData = false;
      vm.addResource = addResource;
      vm.deleteResource = deleteResource;
      vm.ProtectedService = ProtectedService;
      vm.openEditDialog = openEditDialog;

      vm.ProtectedService.getAllProtectedData().then(function(response) {
        vm.protectedData = response;
        if (response.length == 0) {
          vm.noData = true;
          }
        }, function(error) {
          vm.error = true;
          vm.errorHeading = error.data.error;
          vm.errorDescription = error.data.description;
      });

      function addResource() {
        var resourceData = {
          name: vm.name,
          description: vm.description
        }
        vm.ProtectedService.addProtectedData(resourceData).then(function(response) {
          vm.protectedData.push(response);
        });

        vm.name = '';
        vm.description = '';
      }

      // open a modal to update a protected record
      function openEditDialog(item, idx) {
        var modalInstance = $modal.open({
          animation: true,
          templateUrl: 'static/app/protected/edit-protected-resource.html',
          controller: ['$modalInstance', 'item', 'protectedData', 'ProtectedService', 'Restangular', '$state', 'idx', EditModalController],
          controllerAs: 'vm',
          resolve: {
            idx: function() { return idx; },
            protectedData: function() { return vm.protectedData; },
            item: function(Restangular) {
              return Restangular.one('protected_data', item.id).get();            }
            }
        });
      }

      function deleteResource(item, idx) {
        Restangular.one("protected_data", item.id).remove();
        vm.protectedData.splice(idx, 1);
      }


      activate();

      function activate() {

      }
  }

  EditModalController.$inject = ['$modalInstance', 'item', 'protectedData', 'ProtectedService', 'Restangular', '$state', 'idx']
  // the edit form controller to populate the model and update the data
  function EditModalController($modalInstance, item, protectedData, ProtectedService, Restangular, $state, idx) {
    var vm = this;
    var original = item;
    vm.item = Restangular.copy(original);
    vm.protectedData = protectedData;

    vm.updateResource = function() {
      vm.item.put().then(function(updatedItem) {
        vm.protectedData[idx] = updatedItem;
        $modalInstance.close();
      });
    };

  }
})();
