var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;

module.exports = {
    receiveCluster: function (slug, cluster) {
        AppDispatcher.handleAction({
            type: ActionTypes.RECEIVE_CLUSTER,
            slug: slug,
            cluster: cluster
        });
    }
};
