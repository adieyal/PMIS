'use strict';

/* Directives */


angular.module('myApp.directives', ['$strap.directives', 'ui.bootstrap'])
    .controller('AppCtrl', function($scope, $http) {

        $http.get('http://127.0.0.1:8000/api/programmes/', {})
            .success(function(data, status, headers, config) {
                $scope.programmes = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });
        $http.get('http://127.0.0.1:8000/api/districts/', {})
            .success(function(data, status, headers, config) {
                $scope.districts = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get('http://127.0.0.1:8000/api/scope_codes/', {})
            .success(function(data, status, headers, config) {
                $scope.scope_codes = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get('http://127.0.0.1:8000/api/roles/', {})
            .success(function(data, status, headers, config) {
                $scope.roles = data;
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $http.get('http://127.0.0.1:8000/api/entities/', {})
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

        $http.get('http://127.0.0.1:8000/api/milestones/', {})
            .success(function(data, status, headers, config) {
                var l = data.length;
                var res = [];
                $scope.phases = [];
                $scope.milestones = data;
                for (var i=0; i<l; i++){
                    if ($.inArray(data[i].phase, $scope.phases) == -1){
                        $scope.phases.push(data[i].phase)
                    }
                }
            })
            .error(function(data, status, headers, config) {
                $scope.status = status;
            });

        $scope.steps = ['one', 'two', 'three', 'four', 'five', 'six', 'seven'];
        $scope.scopes = ['scope_1'];
        $scope.step = 0;
        $scope.wizard = {};
        $scope.wizard.project = {};
        $scope.wizard.project.municipalities = [];
        $scope.wizard.project_role = {};
//        $scope.years = [
//            { 'name': 'Year 1', 'model': 'year_1'},
//            { 'name': 'Year 2', 'model': 'year_2'},
//            { 'name': 'Year 3', 'model': 'year_3'},
//            { 'name': 'Year 4', 'model': 'year_4'}
//        ];
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

        $scope.month_group();
        $scope.year_items = [ {
                'name': 'Year 1',
                'model': 'year_1',
                'amount': 0,
                'month': [
                    {'name': 'Jan', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Feb', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Mar', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Apr', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'May', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jun', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jul', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Aug', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Sept', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Oct', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Nov', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Dec', 'planning': { 'amount': 0, 'progress': 0 } }
                ]
        },
        {   'name': 'Year 2',
            'model': 'year_2',
            'amount': 0,
            'month': [
                    {'name': 'Jan', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Feb', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Mar', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Apr', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'May', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jun', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jul', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Aug', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Sept', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Oct', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Nov', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Dec', 'planning': { 'amount': 0, 'progress': 0 } }
                ]
            },
            {
                'name': 'Year 3',
                'model': 'year_3',
                'amount': 0,
                'month': [
                    {'name': 'Jan', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Feb', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Mar', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Apr', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'May', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jun', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jul', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Aug', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Sept', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Oct', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Nov', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Dec', 'planning': { 'amount': 0, 'progress': 0 } }
                ]
            },
            {
                'name': 'Year 4',
                'model': 'year_4',
                'amount': 0,
                'month': [
                    {'name': 'Jan', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Feb', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Mar', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Apr', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'May', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jun', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Jul', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Aug', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Sept', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Oct', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Nov', 'planning': { 'amount': 0, 'progress': 0 } },
                    {'name': 'Dec', 'planning': { 'amount': 0, 'progress': 0 } }
                ]
            }
        ];


        $scope.year_group = function(){
            var res=[];
            var l = $scope.year_items.length;
            for(var i=0; i<l;i++){
                if (i % 2 == 0 ){
                    res.push([$scope.year_items[i], $scope.year_items[i+1]])
                }
            }
            $scope.years = res
        };
        $scope.year_group();

        $scope.get_municipality = function(){

            $http.get('http://127.0.0.1:8000/api/districts/'+$scope.wizard.district.id+'/municipalities/', {})
                .success(function(data, status, headers, config) {
                    $scope.municipality_list = data;
                    $scope.wizard.project.municipalities = [];
                })
                .error(function(data, status, headers, config) {
                    $scope.status = status;
                });
        };

        $scope.add = function(){
          $scope.scopes.push('scope_'+String($scope.scopes.length+1));
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

        $scope.handleNext = function(dismiss, is_valid) {
            if($scope.isLastStep()) {
                dismiss();
            } else {
//                if (is_valid) {
                    $scope.step += 1;
//                }
            }
        };
    })
    .directive('autoComplete', function($timeout) {
        return function(scope, iElement, iAttrs) {
            iElement.autocomplete({
                source: scope[iAttrs.uiItems],
                select: function() {
                    $timeout(function() {
                        iElement.trigger('input');
                    }, 0);
                }
            });
        };
    })
    .directive('datepicker', function ($parse) {
    return function (scope, element, attrs, controller) {
        var ngModel = $parse(attrs.ngModel);
        $(function(){
            element.datepicker({
                showOn:"both",
                buttonImage: "../img/calendar.png",
                changeYear:true,
                changeMonth:true,
                dateFormat:'yy-mm-dd',
                onSelect:function (dateText, inst) {
                    scope.$apply(function(scope){
                        // Change binded variable
                        ngModel.assign(scope, dateText);
                    });
                }
            });
        });
    }
}).filter('group', function() {
    return function(input) {
        var group = [];
        var l = input.length;

        for(var i=0; i<l;i++){
            if (i % 2 == 0 ){
                group.push([input[i], input[i+1]])
            }
        }
        return group;
    }
});