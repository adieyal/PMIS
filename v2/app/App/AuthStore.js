var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');
var WebAPIUtils = require('./WebAPIUtils');

function setAuth(auth) {
    localStorage.setItem('auth', JSON.stringify(auth));
}

if (!localStorage.getItem('auth')) {
    setAuth({
        status: 'logged-out'
    });
}

var AuthStore = require('./StoreFactory')(function() {
    this.getState = function() {
        return JSON.parse(localStorage.getItem('auth'));
    };
});

AuthStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    switch(action.type) {
        case ActionTypes.LOGIN:
            setAuth({
                status: 'logged-in',
                auth_token: action.auth_token
            });
            AuthStore.triggerChange();
            break;
        case ActionTypes.LOGIN_FAILURE:
            setAuth({
                status: 'failure',
                data: action.data
            });
            AuthStore.triggerChange();
            break;
        case ActionTypes.LOGOUT:
            setAuth({
                status: 'logged-out'
            });
            AuthStore.triggerChange();
            break;
        default:
            return true;
    }
});

module.exports = AuthStore;
