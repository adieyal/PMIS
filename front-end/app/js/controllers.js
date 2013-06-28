'use strict';

/* Controllers */

angular.module('myApp.controllers', ['ngCookies', 'ui.bootstrap', 'localytics.directives'])
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
        $scope.municipalities = [];
        $scope.wizard.project.municipality = {};
        $scope.wizard.project_role = [];
        $scope.wizard.project_financial = {};
        $scope.wizard.scope_of_work = [{'quantity': "", 'scope_code': {}}];
        $scope.wizard.planning = [];
        $scope.additional_roles = [];
        $scope.add_role = {};
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
                var l = data.length;
                for (var i=0; i<l; i++){
                    $scope.wizard.project_role.push({'role': data[i], 'entity': {}});
                }

            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get(HOST+'/api/entities/', {})
            .success(function(data, status, headers, config) {
                $scope.entities = data;
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
            { 'name': '2013'}

        ];
        $scope.month = [
            {'name': 'Apr', 'id': 4},
            {'name': 'May', 'id': 5},
            {'name': 'Jun', 'id': 6},
            {'name': 'Jul', 'id': 7},
            {'name': 'Aug', 'id': 8},
            {'name': 'Sept', 'id': 9},
            {'name': 'Oct', 'id': 10},
            {'name': 'Nov', 'id': 11},
            {'name': 'Dec', 'id': 12},
            {'name': 'Jan', 'id': 1},
            {'name': 'Feb', 'id': 2},
            {'name': 'Mar', 'id': 3}
        ];


        $scope.create_years_record = function(){
            var l1 = $scope.year_list.length;
            var l2 = $scope.month.length;
            for(var i=0; i<l1; i++){
                $scope.wizard.planning.push($.extend({},
                    $scope.year_list[i],
                    {
                        allocated_budget: "",
                        allocated_planning_budget: "",
                        month: []
                    }
                ));
                for(var j=0; j<l2; j++){
                    $scope.wizard.planning[i].month.push($.extend({},$scope.month[j],{'planning': {
                        'planned_expenses': "",
                        'planned_progress': ""
                    }}));
                }
            }
        };
        $scope.create_years_record();


        $scope.get_municipality = function(){

            $http.get(HOST+'/api/districts/'+$scope.wizard.district.id+'/municipalities/', {})
                .success(function(data, status, headers, config) {
                    $scope.municipalities = data
                    $scope.wizard.project.municipality = {}
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };
        $scope.number = /^\d+$/;
        $scope.year = /^\d{4,4}$/;
        $scope.project_number = /^[\d\w\/]+$/;
        $scope.default = {
            year: ''
        };

        $scope.addYear = function(year, is_valid){
            if (is_valid){
                $scope.default.year = '';
                $scope.year_list.push({'name': year });
                var l2 = $scope.month.length;
                var months = [];
                for(var j=0; j<l2; j++){
                    months.push($.extend({},$scope.month[j],{'planning': {
                        'planned_expenses': "",
                        'planned_progress': ""
                    }}));
                }
                $scope.wizard.planning.push($.extend({},
                    {'name': year},
                    {
                        allocated_budget: "",
                        allocated_planning_budget: "",
                        month: months
                    }
                ));
            }
        };


        $scope.addScopeOfWork = function(){
            $scope.wizard.scope_of_work.push({'quantity': "", 'scope_code': {}});
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
            $http.post(HOST+'/api/projects/', $scope.wizard)
                .success(function(data, status, headers, config) {
                    $location.path('/');
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };
        $scope.handleNext = function(dismiss, is_valid) {
            if (is_valid) {
                if($scope.isLastStep()) {
//                    dismiss();
                    $scope.submitForm();
                } else {
                    $scope.step += 1;
                }
            }
        };
    })
    .controller('ProjectCtrl', ['$scope', '$routeParams', '$http', 'HOST', '$resource', function ($scope, $routeParams, $http, HOST,$resource) {
        $scope.project_id = $routeParams.projectId;
        $http.get(HOST+'/api/projects/'+$scope.project_id+'/', {})
            .success(function(data, status, headers, config) {
                $scope.data = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });
    }])
    .controller('ProjectUpdateCtrl', ['$scope', '$routeParams', '$http', 'HOST', '$location', '$dialog', function ($scope, $routeParams, $http, HOST, $location, $dialog) {
        $scope.steps = ['one', 'two', 'three', 'four'];
        $scope.scopes = ['scope_1'];
        $scope.step = 0;
        var def = {
            'project': {
                'id': '',
                'name': '',
                'description': '',
                'project_number': '',
                'programme': {
                    'id': '',
                    'name': ''
                },
                'municipality': {
                    'id': '',
                    'name': ''
                },
                'project_role': [],
                'scope_of_work': [],
                'planning': [],
                'project_milestones': []

            }
        };
        $scope.wizard = def;
        $scope.municipalities = [];
        $scope.additional_roles = [];
        $scope.add_role = {};

        $scope.project_id = $routeParams.projectId;
        console.log($scope.project_id)
        $http.get(HOST+'/api/projects/'+$scope.project_id+'/', {})
            .success(function(data, status, headers, config) {
                $scope.wizard = data;
                $http.get(HOST+'/api/districts/'+$scope.wizard.project.district+'/municipalities/', {})
                    .success(function(data, status, headers, config) {
                        $scope.municipalities = data
                    })
                    .error(function(data, status, headers, config) {
                        $scope.status = status;
                    });
                $scope.update_years_record();
                $scope.extend_milestones();
                $scope.extend_project_role();
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });


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
        $scope.extend_project_role = function(){
            $http.get(HOST+'/api/roles/', {})
                .success(function(data, status, headers, config) {
                    var l = data.length;
                    var is_enter = false;
                    for (var i=0; i<l; i++){
                        is_enter = false;
                        $.each($scope.wizard.project_roles, function(index, value){
                            if (value.role==data[i].id){
                                is_enter = true;
                            }
                        });
                        if (!is_enter){
                            $scope.wizard.project_roles.push({'role': data[i].id, 'id':'', 'entity': ""});
                        }
                    }
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };

        $http.get(HOST+'/api/entities/', {})
            .success(function(data, status, headers, config) {
                $scope.entities = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $scope.extend_milestones = function(){
            var is_enter = false;
            $http.get(HOST+'/api/milestones/', {})
                .success(function(data, status, headers, config) {
                    var l = data.length;
                    $scope.phases = [];
                    for (var i=0; i<l; i++){
                        data[i].completion_date = "";
                        if ($.inArray(data[i].phase, $scope.phases) == -1){
                            $scope.phases.push(data[i].phase)
                        }
                        is_enter = false;
                        $.each($scope.wizard.project_milestones, function(index, value){
                            if (value.milestone==data[i].id){
                                is_enter = true;
                            }
                        });
                        if (!is_enter){
                            data[i].milestone=data[i].id;
                            delete data[i].id;
                            $scope.wizard.project_milestones.push(data[i])
                        }
                    }
//                    $scope.wizard.project.project_milestones = data;
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };



        $scope.year_list = [
            { 'name': '2013'}

        ];
        $scope.month = [
            {'month_display': 'Apr', 'month': 4},
            {'month_display': 'May', 'month': 5},
            {'month_display': 'Jun', 'month': 6},
            {'month_display': 'Jul', 'month': 7},
            {'month_display': 'Aug', 'month': 8},
            {'month_display': 'Sep', 'month': 9},
            {'month_display': 'Oct', 'month': 10},
            {'month_display': 'Nov', 'month': 11},
            {'month_display': 'Dec', 'month': 12},
            {'month_display': 'Jan', 'month': 1},
            {'month_display': 'Feb', 'month': 2},
            {'month_display': 'Mar', 'month': 3}
        ];

        $scope.planning = [];
        $scope.update_years_record = function(){
            var l2 = $scope.month.length;
            var l3 = $scope.wizard.budgets.length;
            var is_enter = false;
            for(var i=0; i<l3; i++){
                for (var j=0; j<l2; j++){
                    is_enter = false;
                    $.each($scope.wizard.budgets[i].plannings, function(index, value){
                        if ($scope.month[j].month == value.month){
                            is_enter = true
                        }
                    });
                    if (!is_enter){
                        $scope.wizard.budgets[i].plannings.push($.extend({},$scope.month[j],{
                            'planned_expenses': "",
                            'planned_progress': "",
                            'year': $scope.wizard.budgets[i].year
                        }))
                    }
                }
            }
        };



        $scope.get_municipality = function(){

            $http.get(HOST+'/api/districts/'+$scope.wizard.project.district+'/municipalities/', {})
                .success(function(data, status, headers, config) {
                    $scope.municipalities = data
                    $scope.wizard.project.municipality = ''
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };
        $scope.number = /^\d+$/;
        $scope.year = /^\d{4,4}$/;
        $scope.project_number = /^[\d\w\/]+$/;
        $scope.default = {
            year: ''
        };


        $scope.addYear = function(year, is_valid){
            if (is_valid){
                $scope.default.year = '';
                $scope.year_list.push({'year': year });
                var l2 = $scope.month.length;
                var months = [];
                for(var j=0; j<l2; j++){
                    months.push($.extend({},$scope.month[j],{
                        'planned_expenses': "",
                        'planned_progress': "",
                        'year': year
                    }));
                }
                $scope.wizard.budgets.push($.extend({},
                    {'year': year},
                    {
                        allocated_planning_budget: "",
                        allocated_budget: "",
                        plannings: months
                    }
                ));
            }
        };

        $scope.addScopeOfWork = function(){
            $scope.wizard.scope_of_works.push({'quantity': '', 'scope_code': ''});
        };

        $scope.removeScopeOfWork = function(s){
            for (var i = 0, ii = $scope.wizard.scope_of_works.length; i < ii; i++) {
                if (s === $scope.wizard.scope_of_works[i]) {
                    $scope.wizard.scope_of_works.splice(i, 1);
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
        $scope.wizard.update_comment = '';
        $scope.submitForm = function(is_valid){
            if (!$scope.wizard.update_comment){
                $scope.openDialog();
            }else{
                if (is_valid) {
                $http.put(HOST+'/api/projects/'+$scope.project_id+'/', $scope.wizard)
                    .success(function(data, status, headers, config) {
                        $location.path('/');
                    })
                    .error(function(data, status, headers, config) {
                        $scope.status = status;
                    });
                }
            }
        };

        $scope.handleNext = function(dismiss, is_valid) {
            if (!$scope.wizard.update_comment){
                $scope.openDialog();
            }else{
                if (is_valid) {
                    if($scope.isLastStep()) {
//                    dismiss();
                        $scope.submitForm();
                    } else {
                        $scope.step += 1;
                    }
                }
            }

        };
        var t = '<div class="modal-header">'+
            '<h1>Update comment</h1>'+
            '</div>'+
            '<div class="modal-body">'+
            '<div class="row-fluid">'+
            '<textarea class="span12" ng-model="result"></textarea>'+
            '</div>'+
            '</div>'+
            '<div class="modal-footer">'+
            '<button ng-click="close(result)" class="btn btn-primary" >Update project</button>'+
            '</div>';

        $scope.opts = {
            backdrop: true,
            keyboard: true,
            backdropClick: true,
            template:  t, // OR: templateUrl: 'path/to/view.html',
            controller: 'DialogCtl'

        };

        $scope.openDialog = function(){
            var d = $dialog.dialog($scope.opts);
            d.open().then(function(result){
                if(result)
                {
                    $scope.wizard.update_comment = result;
                    $scope.submitForm(true);
                }
            });
        };

    }])
    .controller("DialogCtl", ["$scope", "dialog", function($scope, dialog){
        $scope.close = function(result) {
            dialog.close(result);
        };
    }]);
