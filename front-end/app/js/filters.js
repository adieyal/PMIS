'use strict';

/* Filters */

angular.module('myApp.filters', [])
.filter('is_check', function() {
    return function(input) {
        var res = false
        var l = input.length

        for(var i=0; i<l;i++){
            if (input[i].selected ){
                res = true
            }
        }
        return res;
    }
})
.filter('capitalize', function() {
    return function(input, scope) {
        return input.substring(0,1).toUpperCase()+input.substring(1);
    }
});
