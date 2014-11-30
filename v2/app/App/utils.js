module.exports = {
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
                var index = parseInt((bands.length - 1) * value / (domain[1] - domain[0]));
                return bands[index];
            };
        };
    }
};
