var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;

module.exports = {
    receiveProjects: function (payload) {
        AppDispatcher.handleAction({
            type: ActionTypes.RECEIVE_PROJECTS,
            data: payload.data
        });
    }
};
