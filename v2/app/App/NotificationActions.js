var AppDispatcher = require('./AppDispatcher');
var ActionTypes = require('./Constants').ActionTypes;

module.exports = {
    notify: function (notification) {
        AppDispatcher.handleAction({
            type: ActionTypes.NOTIFY,
            notification: notification
        });
    }
};
