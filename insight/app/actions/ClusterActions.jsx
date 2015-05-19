var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;
var Immutable = require('immutable');

module.exports = {
    receiveCluster: function (cluster) {
        AppDispatcher.handleAction(Immutable.fromJS({
            type: ActionTypes.RECEIVE_CLUSTER,
            cluster: cluster
        }));
    }
};
