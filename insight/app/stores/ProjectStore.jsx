var immstruct = require('immstruct');
var Immutable = require('immutable');
var utils = require('../lib/utils');

var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

var AuthStore = require('./AuthStore');
var PreferenceStore = require('./PreferenceStore');

var store = immstruct({
    projects: []
});

store.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    AppDispatcher.waitFor([
        AuthStore.dispatchToken,
        PreferenceStore.dispatchToken
    ]);

    switch(action.type) {
        case ActionTypes.RECEIVE_PROJECTS:
            store.cursor('projects').update(() => Immutable.fromJS(action.projects));
            break;
        case ActionTypes.SET_DATE:
            var preference = PreferenceStore.cursor();

            remote.fetchProjects(AuthStore.cursor().get('authToken'), {
                year: preference.get('year'),
                month: preference.get('month')
            });
            break;
        default:
    }
});

if (typeof window != 'undefined') {
    var remote = require('../lib/remote');
    var preference = PreferenceStore.cursor();
    remote.fetchProjects(AuthStore.cursor().get('authToken'), {
        year: preference.get('year'),
        month: preference.get('month')
    });
}

module.exports = store;
