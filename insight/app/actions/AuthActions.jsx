var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;
var Immutable = require('immutable');

module.exports = {
    login: function(authToken) {
        AppDispatcher.handleAction(Immutable.fromJS({
            type: ActionTypes.LOGIN,
            authToken: authToken
        }));
    },
    loginFailure: function(data) {
        AppDispatcher.handleAction(Immutable.fromJS({
            type: ActionTypes.LOGIN_FAILURE,
            data: data
        }));
    },
    logout: function() {
        AppDispatcher.handleAction(Immutable.fromJS({
            type: ActionTypes.LOGOUT
        }));
    }
};
