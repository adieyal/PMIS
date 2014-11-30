var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;

module.exports = {
    login: function(auth_token) {
        AppDispatcher.handleAction({
            type: ActionTypes.LOGIN,
            auth_token: auth_token
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
