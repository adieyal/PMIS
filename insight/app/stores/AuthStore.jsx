var immstruct = require('immstruct');
var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

function setAuth(auth) {
    localStorage.setItem('auth', JSON.stringify(auth));
}

var defaultAuthState = {
    status: 'logged-out'
};

var state = typeof localStorage == 'undefined' ? defaultAuthState : JSON.parse(localStorage.getItem('auth'));

if (typeof localStorage != 'undefined' && !localStorage.getItem('auth')) {
    setAuth(defaultAuthState);
}

var store = immstruct(state);

store.dispatchToken = AppDispatcher.register(function(payload) {
    var cursor = store.cursor();
    var action = payload.get('action');
    var ActionTypes = Constants.ActionTypes;

    switch(action.get('type')) {
        case ActionTypes.LOGIN:
            cursor.update(function(current) {
                setAuth({
                    status: 'logged-in',
                    authToken: action.get('authToken')
                });

                return current
                    .set('status', 'logged-in')
                    .set('authToken', action.get('authToken'));
            });
            break;
        case ActionTypes.LOGIN_FAILURE:
            cursor.update(function(current) {
                setAuth({
                    status: 'failure'
                });

                return current
                    .remove('authToken')
                    .set('status', 'failure')
                    .set('data', action.get('data'));
            });
            break;
        case ActionTypes.LOGOUT:
            cursor.update(function(current) {
                setAuth({
                    status: 'logged-out'
                });

                return current
                    .remove('data')
                    .remove('authToken')
                    .set('status', 'logged-out');
            });
            break;
        default:
            return true;
    }
});

module.exports = store;
