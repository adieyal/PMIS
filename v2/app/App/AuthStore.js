var _ = require('lodash');
var EventEmitter = require('events').EventEmitter;
var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');
var WebAPIUtils = require('./WebAPIUtils');
var store = require('store2');

if (!store.session.has('auth')) {
    store.session.set('auth', {
        status: 'logged-out'
    });
}

var AuthStore = _.merge({}, EventEmitter.prototype, {
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
        return store.session('auth');
    }
});

AuthStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    switch(action.type) {
        case ActionTypes.LOGIN:
            store.session.set('auth', {
                status: 'logged-in',
                auth_token: action.auth_token
            }, true);
            AuthStore.emitChange();
            break;
        case ActionTypes.LOGIN_FAILURE:
            store.session.set('auth', {
                status: 'failure',
                data: action.data
            }, true);
            AuthStore.emitChange();
            break;
        case ActionTypes.LOGOUT:
            store.session.set('auth', {
                status: 'logged-out'
            }, true);
            AuthStore.emitChange();
            break;
        default:
            return true;
    }
});

module.exports = AuthStore;
