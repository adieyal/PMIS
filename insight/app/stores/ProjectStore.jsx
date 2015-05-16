var utils = require('../lib/utils');
var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var ProjectActions = require('../actions/ProjectActions');
var StoreFactory = require('./StoreFactory');
var AuthStore = require('./AuthStore');
var PreferenceStore = require('./PreferenceStore');

var state = {
    projects: []
};

var ProjectStore = StoreFactory(function() {
    this.getState = function() {
        return state;
    };
});

ProjectStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    AppDispatcher.waitFor([
        AuthStore.dispatchToken
    ]);

    switch(action.type) {
        case ActionTypes.RECEIVE_PROJECTS:
            state.projects = action.data;
            ProjectStore.triggerChange();
            break;
        case ActionTypes.SET_DATE:
            AppDispatcher.waitFor([
                PreferenceStore.dispatchToken
            ]);

            var preference = PreferenceStore.getState();

            remote.fetchProjects(AuthStore.getState().authToken, { year: preference.year, month: preference.month });
            break;
        default:
    }
});

if (typeof window != 'undefined') {
    var remote = require('../lib/remote');
    var preference = PreferenceStore.getState();
    remote.fetchProjects(AuthStore.getState().authToken, { year: preference.year, month: preference.month });
}

module.exports = ProjectStore;
