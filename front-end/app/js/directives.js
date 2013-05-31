'use strict';

/* Directives */


angular.module('myApp.directives', ['$strap.directives'])
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

        $scope.steps = ['one', 'two', 'three', 'four', 'five', 'six', 'seven'];
        $scope.scopes = ['scope_1'];
        $scope.step = 0;
        $scope.wizard = {};
        $scope.wizard.municipalities = [];

        $scope.get_municipality = function(){

            $http.get('http://127.0.0.1:8000/api/districts/'+$scope.wizard.district.id+'/municipalities/', {})
                .success(function(data, status, headers, config) {
                    $scope.municipalities = data;
                    $scope.wizard.municipalities = [];
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

        $scope.handleNext = function(dismiss) {
            if($scope.isLastStep()) {
                dismiss();
            } else {
//                console.log($scope.step_one)
//                if ($scope.step_one) {
                    $scope.step += 1;
//                }
            }
        };
    }).directive('autoComplete', function($timeout) {
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
    });
