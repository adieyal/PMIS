var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;

module.exports = {
    notify: function (notification) {
        AppDispatcher.handleAction({
            type: ActionTypes.NOTIFY,
            notification: notification
        });
    }
};
