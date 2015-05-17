var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var StoreFactory = require('./StoreFactory');
var immstruct = require('immstruct');

var today = new Date();
var month = today.getMonth() + 1;

if(month < 10) {
    month = '0' + month;
}

var store = immstruct({
    view: 'dashboard',
    order: 'alphabetic',
    year: today.getFullYear(),
    month: month
});

store.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;
    var cursor = store.cursor();

    switch(action.type) {
        case ActionTypes.SET_PREFERENCE:
            cursor.update(action.key, () => action.value);
            break;
        case ActionTypes.SET_DATE:
            cursor.update((curr) =>
                curr.set('year', action.year).set('month', action.month)
            );
            break;
        default:
    }
});

module.exports = store;
