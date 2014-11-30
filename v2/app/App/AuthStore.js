var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');

function setAuth(auth) {
    localStorage.setItem('auth', JSON.stringify(auth));
}

var defaultAuthState = {
    status: 'logged-out'
};

if (typeof localStorage != 'undefined' && !localStorage.getItem('auth')) {
    setAuth(defaultAuthState);
}

var AuthStore = require('./StoreFactory')(function() {
    this.getState = function() {
        var state = typeof localStorage == 'undefined' ? defaultAuthState : JSON.parse(localStorage.getItem('auth'));
        return state;
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
