var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var StoreFactory = require('./StoreFactory');
var PreferenceStore = require('./PreferenceStore');

var state = {
    notifications: []
};

var NotificationStore = StoreFactory(function() {
    this.getLastNotification = function() {
        return state.notifications[state.notifications.length - 1];
    };

    this.getState = function() {
        return state;
    };
});

NotificationStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    AppDispatcher.waitFor([
        PreferenceStore.dispatchToken
    ]);

    switch(action.type) {
        case ActionTypes.NOTIFY:
            state.notifications.push(action.notification);
            NotificationStore.triggerChange();
            break;
        default:
            return true;
    }
});

module.exports = NotificationStore;
