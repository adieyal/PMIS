var keyMirror = require('keymirror');

module.exports = {
    CHANGE_EVENT: 'change',

    ActionTypes: keyMirror({
        FETCH_CLUSTER: null,
        RECEIVE_CLUSTER: null,

        LOGIN: null,
        LOGIN_FAILURE: null,
        LOGGED_IN: null,
        LOGOUT: null,
        LOGGED_OUT: null,

        NOTIFY: null,

        SET_PREFERENCE: null
    })
};
