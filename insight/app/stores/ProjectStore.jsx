var immstruct = require('immstruct');

var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

var AuthStore = require('./AuthStore');
var PreferenceStore = require('./PreferenceStore');

var store = immstruct({
    projects: []
});

store.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.get('action');
    var ActionTypes = Constants.ActionTypes;

    AppDispatcher.waitFor([
        AuthStore.dispatchToken,
        PreferenceStore.dispatchToken
    ]);

    switch(action.get('type')) {
        case ActionTypes.RECEIVE_PROJECTS:
            store.cursor('projects').update(() => action.get('projects'));
            break;
        case ActionTypes.SET_DATE:
            var preference = PreferenceStore.cursor();

            remote.fetchProjects(AuthStore.cursor().get('authToken'),
                                 preference.get('year'));
            break;
        default:
    }
});

if (typeof window != 'undefined') {
    var remote = require('../lib/remote');
    var preference = PreferenceStore.cursor();
    remote.fetchProjects(AuthStore.cursor().get('authToken'),
                         preference.get('year'));
}

module.exports = store;
