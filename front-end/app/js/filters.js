'use strict';

/* Filters */

angular.module('myApp.filters', [])
    .filter('group', function() {
        return function(input) {
            var g = [];
            var l = input.length;

            for(var i=0; i<l;i++){
                if (i % 2 == 0 ){
                    g.push([input[i], input[i+1]])
                }
            }
            console.log(g)
            return g;
        }
    });
