'use strict';

var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;

module.exports = {
    setDate: function(year, month) {
        AppDispatcher.handleAction({
            type: ActionTypes.SET_DATE,
            year: year,
            month: month
        });
    },
    setPreference: function(key, value) {
        AppDispatcher.handleAction({
            type: ActionTypes.SET_PREFERENCE,
            key: key,
            value: value
        });
    }
};
