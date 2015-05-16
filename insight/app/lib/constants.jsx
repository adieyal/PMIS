var utils = require('../lib/utils');

module.exports = {
    CHANGE_EVENT: 'change',

    ActionTypes: utils.keyMirror([
        'RECEIVE_CLUSTER',
        'RECEIVE_RESULTS',
        'RECEIVE_PROJECTS',

        'LOGIN',
        'LOGIN_FAILURE',
        'LOGGED_IN',
        'LOGOUT',
        'LOGGED_OUT',

        'NOTIFY',

        'SET_PREFERENCE',
        'SET_DATE'
    ])
};
