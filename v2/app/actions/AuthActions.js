var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;

module.exports = {
    login: function(authToken) {
        AppDispatcher.handleAction({
            type: ActionTypes.LOGIN,
            authToken: authToken
        });
    },
    loginFailure: function(data) {
        AppDispatcher.handleAction({
            type: ActionTypes.LOGIN_FAILURE,
            data: data
        });
    },
    logout: function() {
        AppDispatcher.handleAction({
            type: ActionTypes.LOGOUT
        });
    }
};
