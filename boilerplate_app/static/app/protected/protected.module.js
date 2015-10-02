(function() {
  'use strict';
  angular
    .module('boilerplate.protected', [
      'restangular',
      'ngMessages',
      'angular-loading-bar'
    ])
    .config(function(RestangularProvider) {
      RestangularProvider.setBaseUrl('http://127.0.0.1:5000/api/v1');
      // configure the response extractor for each request 
      RestangularProvider.setResponseExtractor(function(response, operation) { 
        // This is a get for a list 
        var newResponse; 
        if (operation === 'getList') { 
          // Return the result objects as an array and attach the metadata 
          newResponse = response.objects; 
          newResponse.metadata = { 
            numResults: response.num_results, 
            page: response.page, 
            totalPages: response.total_pages 
          }; 
        } else { 
          // This is an element 
          newResponse = response; 
        } 
        return newResponse;
      }); 
    });
})();
