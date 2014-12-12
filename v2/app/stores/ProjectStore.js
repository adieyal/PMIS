var utils = require('../lib/utils');
var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var ProjectActions = require('../actions/ProjectActions');
var StoreFactory = require('./StoreFactory');
var AuthStore = require('./AuthStore');

var state = [];

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
            state = action.data;
            ProjectStore.triggerChange();
            break;
        default:
    }
});

if (typeof window != 'undefined') {
    var remote = require('../lib/remote');
    remote.fetchProjects(AuthStore.getState().authToken, ProjectActions.receiveProjects);
}

module.exports = ProjectStore;
