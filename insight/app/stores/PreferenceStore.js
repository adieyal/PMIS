var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var StoreFactory = require('./StoreFactory');

var today = new Date();
var month = today.getMonth() + 1;

if(month < 10) {
    month = '0' + month;
}

var state = {
    order: 'alphabetic',
    year: today.getFullYear(),
    month: month
};

var PreferenceStore = StoreFactory(function() {
    this.getState = function() {
        return state;
    };
});

PreferenceStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    switch(action.type) {
        case ActionTypes.SET_PREFERENCE:
            state[action.key] = action.value;
            PreferenceStore.triggerChange();
            break;
        case ActionTypes.SET_DATE:
            state.year = action.year;
            state.month = action.month;
            PreferenceStore.triggerChange();
            break;
        default:
    }
});

module.exports = PreferenceStore;
