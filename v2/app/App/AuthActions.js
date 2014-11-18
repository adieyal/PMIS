var AppDispatcher = require('./AppDispatcher');
var ActionTypes = require('./Constants').ActionTypes;
var WebAPIUtils = require('./WebAPIUtils');

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
