var keyMirror = require('keymirror');

module.exports = {
    CHANGE_EVENT: 'change',

    ActionTypes: keyMirror({
        RECEIVE_CLUSTER: null,

        RECEIVE_RESULTS: null,

        LOGIN: null,
        LOGIN_FAILURE: null,
        LOGGED_IN: null,
        LOGOUT: null,
        LOGGED_OUT: null,

        NOTIFY: null,

        SET_PREFERENCE: null
    })
};
