var _ = require('lodash');
var EventEmitter = require('events').EventEmitter;
var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');

var state = {
    notifications: []
};

var NotificationStore = _.merge({}, EventEmitter.prototype, {
    addChangeListener: function(done) {
        this.on(Constants.CHANGE_EVENT, done);
    },
    removeChangeListener: function(done) {
        this.removeListener(Constants.CHANGE_EVENT, done);
    },
    emitChange: function() {
        this.emit(Constants.CHANGE_EVENT);
    },
    getLastNotification: function() {
        return _.last(state.notifications);
    },
    getState: function() {
        return state;
    }
});

NotificationStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    switch(action.type) {
        case ActionTypes.NOTIFY:
            state.notifications.push(action.notification);
            NotificationStore.emitChange();
            break;
        default:
            return true;
    }
});

module.exports = NotificationStore;
