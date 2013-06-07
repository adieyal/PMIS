'use strict';

/* Controllers */

angular.module('myApp.controllers', ['ngCookies'])
    .controller('MyCtrl1', ['$scope', '$http', '$routeParams', 'HOST', function($scope, $http, $routeParams, HOST) {
        $http.defaults.useXDomain = true;
//        $scope.name = "BookCntl";
        $scope.params = $routeParams;
        $http.get(HOST+"/api/projects/",{headers: {

        }})
            .success(function(data, status, headers, config) {
                $scope.projects = data;

            }).error(function(data, status, headers, config) {
                $scope.status = status;
            });
    }])
    .controller('MyCtrl2', ['$scope', '$http', '$rootScope', '$cookieStore', '$location', 'HOST', function($scope, $http, $rootScope, $cookieStore, $location, HOST) {
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
            $http.post(HOST+'/api-token-auth/', {
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

    }])
    .config(['$httpProvider', function($httpProvider) {
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

    }])
    .controller('AppCtrl', function($scope, $http, HOST, $location) {
        $scope.steps = ['one', 'two', 'three', 'four'];
        $scope.scopes = ['scope_1'];
        $scope.step = 0;
        $scope.wizard = {};
        $scope.wizard.project = {};
        $scope.wizard.project.municipalities = [];
        $scope.wizard.project_role = {};
        $scope.wizard.project_financial = {};
        $scope.wizard.scope_of_work = [{'quantity': "", 'scope_code': ""}];
        $scope.wizard.planning = [];
        $http.get(HOST+'/api/programmes/', {})
            .success(function(data, status, headers, config) {
                $scope.programmes = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });
        $http.get(HOST+'/api/districts/', {})
            .success(function(data, status, headers, config) {
                $scope.districts = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get(HOST+'/api/scope_codes/', {})
            .success(function(data, status, headers, config) {
                $scope.scope_codes = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get(HOST+'/api/roles/', {})
            .success(function(data, status, headers, config) {
                $scope.roles = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get(HOST+'/api/entities/', {})
            .success(function(data, status, headers, config) {
                var l = data.length;
                $scope.entities = [];
                for (var i=0; i<l; i++){
                    $scope.entities.push(data[i].name);
                }
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get(HOST+'/api/milestones/', {})
            .success(function(data, status, headers, config) {
                var l = data.length;
                $scope.phases = [];
                for (var i=0; i<l; i++){
                    data[i].completion_date = "";
                    if ($.inArray(data[i].phase, $scope.phases) == -1){
                        $scope.phases.push(data[i].phase)
                    }
                }
                $scope.wizard.project_milestones = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });


        $scope.year_list = [
            { 'name': 'Year 1', 'model': 'year_1'},
            { 'name': 'Year 2', 'model': 'year_2'},
            { 'name': 'Year 3', 'model': 'year_3'},
            { 'name': 'Year 4', 'model': 'year_4'}
        ];
        $scope.month = [
            {'name': 'Jan'},
            {'name': 'Feb'},
            {'name': 'Mar'},
            {'name': 'Apr'},
            {'name': 'May'},
            {'name': 'Jun'},
            {'name': 'Jul'},
            {'name': 'Aug'},
            {'name': 'Sept'},
            {'name': 'Oct'},
            {'name': 'Nov'},
            {'name': 'Dec'}];

        $scope.month_group = function(){
            var res=[];
            var l = $scope.month.length;
            for(var i=0; i<l;i++){
                if (i % 2 == 0 ){
                    res.push([$scope.month[i], $scope.month[i+1]])
                }
            }
            $scope.months = res
        };
        $scope.create_years_record = function(){
            var l1 = $scope.year_list.length;
            var l2 = $scope.month.length;
            for(var i=0; i<l1; i++){
                $scope.wizard.planning.push($.extend({},
                    $scope.year_list[i],
                    {
                        amount: "",
                        month: []
                    }
                ));
                for(var j=0; j<l2; j++){
                    $scope.wizard.planning[i].month.push($.extend({},$scope.month[j],{'planning': {
                        'amount': "",
                        'progress': ""
                    }}));
                }
            }
        };
        $scope.create_years_record();
        $scope.month_group();


        $scope.year_group = function(){
            var res=[];
            var l = $scope.wizard.planning.length;
            for(var i=0; i<l;i++){
                if (i % 2 == 0 ){
                    res.push([$scope.wizard.planning[i], $scope.wizard.planning[i+1]])
                }
            }
            $scope.years = res
        };
        $scope.year_group();

        $scope.get_municipality = function(){

            $http.get(HOST+'/api/districts/'+$scope.wizard.district.id+'/municipalities/', {})
                .success(function(data, status, headers, config) {
//                    $scope.municipality_list = data;
//                    $scope.wizard.project.municipalities = [];
                    var res = [];
                    var l = data.length;
                    for (var i=0; i<l; i++){
                        data[i].selected=false;
//                        res.push(data[i].selected=false)
                    }
                    $scope.wizard.project.municipalities = data
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };
        $scope.number = /^\d+$/;
        $scope.addScopeOfWork = function(){
            $scope.wizard.scope_of_work.push({'quantity': "", 'scope_code': ""});
        };
        $scope.removeScopeOfWork = function(s){
            for (var i = 0, ii = $scope.wizard.scope_of_work.length; i < ii; i++) {
                if (s === $scope.wizard.scope_of_work[i]) {
                    $scope.wizard.scope_of_work.splice(i, 1);
                }
            }
        };
        $scope.isFirstStep = function() {
            return $scope.step === 0;
        };

        $scope.isLastStep = function() {
            return $scope.step === ($scope.steps.length - 1);
        };

        $scope.isCurrentStep = function(step) {
            return $scope.step === step;
        };

        $scope.setCurrentStep = function(step) {
            $scope.step = step;
        };

        $scope.getCurrentStep = function() {
            return $scope.steps[$scope.step];
        };

        $scope.getNextLabel = function() {
            return ($scope.isLastStep()) ? 'Submit' : 'Next';
        };

        $scope.handlePrevious = function() {
            $scope.step -= ($scope.isFirstStep()) ? 0 : 1;
        };

        $scope.submitForm = function(){
            $http.post(HOST+'/api/create_project/', $scope.wizard)
                .success(function(data, status, headers, config) {
                    $location.path('/');
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };
        $scope.handleNext = function(dismiss, is_valid) {
//            if (is_valid) {
                if($scope.isLastStep()) {
//                    dismiss();
                    $scope.submitForm();
                } else {
                    $scope.step += 1;
                }
//            }
        };
    })