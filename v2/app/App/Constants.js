function keyMirror(keys) {
    var values = {};
    keys.forEach(function (key) {
        values[key] = key;
    });
    return values;
}

module.exports = {
    CHANGE_EVENT: 'change',

    ActionTypes: keyMirror([
        'RECEIVE_CLUSTER',

        'RECEIVE_RESULTS',

        'LOGIN',
        'LOGIN_FAILURE',
        'LOGGED_IN',
        'LOGOUT',
        'LOGGED_OUT',

        'NOTIFY',

        'SET_PREFERENCE'
    ])
};
