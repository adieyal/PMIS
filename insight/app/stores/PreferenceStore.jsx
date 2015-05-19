var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var immstruct = require('immstruct');

var today = new Date();
var month = today.getMonth();
var year = today.getFullYear();

/** Month 3 is April (0-based) */
if (month < 3) {
    year--;
}
var store = immstruct({
    view: 'dashboard',
    order: 'alphabetic',
    year: year
});


store.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.get('action');
    var ActionTypes = Constants.ActionTypes;
    var cursor = store.cursor();

    switch(action.get('type')) {
        case ActionTypes.SET_PREFERENCE:
            cursor.update(action.get('key'), () => action.get('value'));
            break;
        case ActionTypes.SET_FINANCIAL_YEAR:
            cursor.update('year', (curr) => action.get('year'))
            break;
        default:
    }
});

module.exports = store;
