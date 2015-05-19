var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;
var Immutable = require('immutable');

module.exports = {
    notify: function (notification) {
        AppDispatcher.handleAction(Immutable.fromJS({
            type: ActionTypes.NOTIFY,
            notification: notification
        }));
    }
};
