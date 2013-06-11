'use strict';

/* Filters */

angular.module('myApp.filters', [])
.filter('is_check', function() {
    return function(input) {
        for (var prop in input) if (input.hasOwnProperty(prop)) return true;
        return false;
    }
})
.filter('capitalize', function() {
    return function(input, scope) {
        return input.substring(0,1).toUpperCase()+input.substring(1);
    }
})
.filter('range', function() {
    return function(input, total) {
        total = parseInt(total);
        for (var i=0; i<total; i++)
            input.push(i);
        return input;
    };
});

