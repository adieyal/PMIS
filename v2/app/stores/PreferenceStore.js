var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var StoreFactory = require('./StoreFactory');

var state = {
    order: 'alphabetic'
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
        default:
    }
});

module.exports = PreferenceStore;
