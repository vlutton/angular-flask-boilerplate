(function() {
  'use strict';

  angular
      .module('boilerplate.auth')
      .factory('AuthService', AuthService);

  AuthService.$inject = ['$auth', '$state', '$http', 'API', '$rootScope', '$q'];
  function AuthService($auth, $state, $http, API, $rootScope, $q) {
      var Auth = {
        register: register,
        login: login,
        logout: logout,
        saveUser: saveUser,
        getStorageMethod: getStorageMethod,
        regStatus: null,
        regStatusMessage: null,
        registered: null,
        storageMethod: 'localStorage'
      };

      return Auth;

      function register(email, username, password) {
        return $http.post(API + '/users/', {
          email: email,
          username: username,
          password: password
        });
      }

      function saveUser(user) {
        $http.get(API+'/api/v1/user/'+user.user_id).then(function(userResponse) {
          var userString = JSON.stringify(userResponse.data);
          if (Auth.storageMethod == "localStorage") {
            localStorage.setItem("user", userString);
          } else {
            sessionStorage.setItem("user", userString);
          }
          $rootScope.authenticated = true;
          $rootScope.currentUser = userResponse.data;
        });
      }

      function login(credentials, remember_me) {
        if (remember_me == true) {
          Auth.storageMethod = 'localStorage';
        } else {
          Auth.storageMethod = 'sessionStorage';
        }

        $auth.setStorageType(this.storageMethod);
        var deferred = $q.defer();
        $auth.login(credentials).then(function(response) {
          var user = $auth.getPayload();
          deferred.resolve(user);
        }, function(response) {
          return deferred.reject(response);
        });

        return deferred.promise;
      }

      function logout() {
        $auth.logout().then(function() {
            // Remove the authenticated user from local storage
            localStorage.removeItem('user');

            // Flip authenticated to false so that we no longer
            // show UI elements dependant on the user being logged in
            $rootScope.authenticated = false;

            // Remove the current user info from rootscope
            $rootScope.currentUser = null;
        });
      }

      function getStorageMethod() {
        return Auth.storageMethod;
      }

  }
})();
