var _ = require('lodash');
var EventEmitter = require('events').EventEmitter;
var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');

var state = {
    order: 'alphabetic'
};

var PreferenceStore = _.merge({}, EventEmitter.prototype, {
    addChangeListener: function(done) {
        this.on(Constants.CHANGE_EVENT, done);
    },
    removeChangeListener: function(done) {
        this.removeListener(Constants.CHANGE_EVENT, done);
    },
    emitChange: function() {
        this.emit(Constants.CHANGE_EVENT);
    },
    getState: function() {
        return state;
    }
});

PreferenceStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    switch(action.type) {
        case ActionTypes.SET_PREFERENCE:
            state[action.key] = action.value;
            PreferenceStore.emitChange();
            break;
        default:
    }
});

module.exports = PreferenceStore;
