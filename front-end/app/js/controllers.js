'use strict';

/* Controllers */

angular.module('myApp.controllers', []).
    controller('MyCtrl1', ['$scope', '$http', function($scope, $http) {
        $http.defaults.useXDomain = true;

        $http.get("http://127.0.0.1:8000/api/projects/",{headers: {

        }})
            .success(function(data, status, headers, config) {
                $scope.projects = data;

            }).error(function(data, status, headers, config) {
                $scope.status = status;
            });
    }])
    .controller('MyCtrl2', ['$scope', '$http', '$rootScope',  function($scope, $http, $rootScope) {
        $http.defaults.useXDomain = true;
        $rootScope.is_auth = false;
        $scope.login = function() {
            $http.post('http://127.0.0.1:8000/api-token-auth/', {
                "username": $scope.username,
                "password": $scope.password
            }).success(function(data, status, headers, config) {

                    $http.defaults.headers.common['Authorization'] = "Token "+data.token;
                    $rootScope.is_auth = true;

                }).error(function(data, status, headers, config) {
                    if (404 === status) {
                        $scope.invalidUsernamePassword = true; // <--------------
                    }
                });
            return false;
        };
        $scope.logout = function(){
            delete $http.defaults.headers.common['Authorization'];
            $rootScope.is_auth = false;
        }

    }]) .config(['$httpProvider', function($httpProvider) {
        delete $httpProvider.defaults.headers.common["X-Requested-With"]
    }]);