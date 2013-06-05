'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives', 'myApp.controllers'])
.value('HOST','http://127.0.0.1:8000')
.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $routeProvider.when('/api/projects/', {templateUrl: '/partials/projects.html', controller: 'MyCtrl1'});
    $routeProvider.when('/login/', {templateUrl: '/partials/login.html', controller: 'MyCtrl2'});
    $routeProvider.when('/', {templateUrl: '/partials/home.html', controller: 'MyCtrl3'});
    $routeProvider.when('/about/', {templateUrl: '/partials/about.html', controller: 'MyCtrl4'});
    $routeProvider.when('/contact/', {templateUrl: '/partials/contact.html', controller: 'MyCtrl5'});
    $routeProvider.when('/create_project/', {templateUrl: '/partials/form_create_project.html', controller: 'AppCtrl'});
    $routeProvider.otherwise();
    $locationProvider.html5Mode(true);
}]);
