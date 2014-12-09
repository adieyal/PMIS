module.exports = {
    iterate: function(arr, func, done) {
        if (arr.length === 0) {
            if (typeof done !== 'undefined') {
                return done();
            }

            return;
        }

        var item = arr[0];

        return func(item, function() {
            return this.iterate(arr.slice(1), func, done);
        }.bind(this));
    },
    join: function (glue, arr) {
        var l = arr.length;
        return this.flatten(this.map(arr, function (item, index) {
            return index < (l - 1) ? [ item, glue ] : item;
        }));
    },
    inspector: function() {
        console.dir(arguments);
    },
    find: function(arr, filter) {
        for (var x=0, l=arr.length; x < l; x++) {
            var item = arr[x];
            if (filter(item)) return item;
        }
    },
    each: function (thing, func) {
        if (typeof thing == 'object') {
            return Object.keys(thing).forEach(function (key) {
                func(thing[key], key, thing);
            });
        }

        thing.forEach(func);
    },
    map: function (thing, func) {
        if (typeof thing == 'object') {
            return Object.keys(thing).map(function (key) {
                return func(thing[key], key, thing);
            });
        }

        return thing.map(func);
    },
    extend: function (a, b) {
        for (var key in b) {
            if (b.hasOwnProperty(key)) {
                a[key] = b[key];
            }
        }

        return a;
    },
    pluck: function (thing, attr) {
        if (typeof thing == 'object') {
            var keys = Object.keys(thing);
            return keys.map(function (key) {
                return thing[key][attr];
            });
        }

        return thing.map(function (item) {
            return item[attr];
        });
    },
    max: function (arr) {
        return arr.reduce(function (acc, item) {
            return Math.max(acc, item);
        });
    },
    flatten: function (arr) {
        return arr.reduce(function (acc, item) {
            if (item instanceof Array) {
                item.forEach(function (innerItem) {
                    acc.push(innerItem);
                });
            } else {
                acc.push(item);
            }
            return acc;
        }, []);
    },
    values: function (thing) {
        if (typeof thing == 'object') {
            return Object.keys(thing).map(function (key) {
                return thing[key];
            });
        }

        return thing.values();
    },
    scale: function (bands) {
        return function(domain) {
            return function(value) {
                var result = (bands.length - 1) * value / (domain[1] - domain[0]);
                return Math.round(result);
            };
        };
    },
    ranges: function(bands, domain) {
        var result = [];

        var scale = this.scale(bands)(domain);

        var mins = {};
        var maxs = {};

        for(var x = domain[0]; x <= domain[1]; x++) {
            var which = scale(x);
            mins[which] = typeof mins[which] == 'undefined' ? x : Math.min(mins[which], x);
            maxs[which] = typeof maxs[which] == 'undefined' ? x : Math.max(maxs[which], x);
        }

        for(var y = 0, l = bands.length; y < l; y++) {
            result.push({
                band: bands[y],
                min: mins[y],
                max: maxs[y]
            });
        }

        return result;
    },
    keyMirror: function (keys) {
        return keys.reduce(function (values, key) {
            values[key] = key;
            return values;
        }, {});
    }
};
