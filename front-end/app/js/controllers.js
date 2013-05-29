'use strict';

/* Controllers */

angular.module('myApp.controllers', ['ngCookies']).
    controller('MyCtrl1', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
        $http.defaults.useXDomain = true;
//        $scope.name = "BookCntl";
        $scope.params = $routeParams;
        $http.get("http://127.0.0.1:8000/api/projects/",{headers: {

        }})
            .success(function(data, status, headers, config) {
                $scope.projects = data;

            }).error(function(data, status, headers, config) {
                $scope.status = status;
            });
    }])
    .controller('MyCtrl2', ['$scope', '$http', '$rootScope', '$cookieStore', '$location', function($scope, $http, $rootScope, $cookieStore, $location) {
        $http.defaults.useXDomain = true;
        $rootScope.is_auth = function(){
            var token = $cookieStore.get('token');
            var user = $cookieStore.get('user');
            if (token){
                $http.defaults.headers.common['Authorization'] = token;
                if (user){
                    $rootScope.user = user;
                }else{
                    $rootScope.user = 'Undefined'
                }
                return true
            }else{
                return false
            }
        };
        $scope.login = function() {
            $http.post('http://127.0.0.1:8000/api-token-auth/', {
                "username": $scope.username,
                "password": $scope.password
            }).success(function(data, status, headers, config) {
                    if (data.token){
                        $http.defaults.headers.common['Authorization'] = "Token "+data.token;
                        $cookieStore.put('token', "Token "+data.token)
                        $cookieStore.put('user', $scope.username)
                        $location.path('/');
                    }

                }).error(function(data, status, headers, config) {
                    if (404 === status) {
                        $scope.invalidUsernamePassword = true; // <--------------
                    }
                    if (data.non_field_errors){
                        $scope.non_field_errors = true;
                    }
                });
            return false;
        };
        $scope.logout = function(){
            delete $http.defaults.headers.common['Authorization'];
            $cookieStore.remove('token');
            $cookieStore.remove('user');
            $location.path('/');
        }

    }]) .config(['$httpProvider', function($httpProvider) {
        delete $httpProvider.defaults.headers.common["X-Requested-With"]
    }])
    .controller('MainCntl', ['$scope', '$route', '$routeParams', '$location', function ($scope, $route, $routeParams, $location) {
        $scope.$route = $route;
        $scope.$location = $location;
        $scope.$routeParams = $routeParams;
    }])
    .controller('MyCtrl3', ['$scope', function ($scope) {

    }])
    .controller('MyCtrl4', ['$scope', function ($scope) {

    }])
    .controller('MyCtrl5', ['$scope', function ($scope) {

    }]);