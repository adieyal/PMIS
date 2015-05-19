var immstruct = require('immstruct');
var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var PreferenceStore = require('./PreferenceStore');

var store = immstruct({
    notifications: []
});

store.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.get('action');
    var ActionTypes = Constants.ActionTypes;

    AppDispatcher.waitFor([
        PreferenceStore.dispatchToken
    ]);

    switch(action.get('type')) {
        case ActionTypes.NOTIFY:
            var humane = require('humane-js');
            var notify = humane.create();
            notify.log(notifications[notifications.length-1]);
            store.cursor('notifications').push(action.get('notification'));
            break;
        default:
            return true;
    }
});

module.exports = store;
