var AppDispatcher = require('./AppDispatcher');
var ActionTypes = require('./Constants').ActionTypes;
var WebAPIUtils = require('./WebAPIUtils');

module.exports = {
    receiveCluster: function (slug, cluster) {
        AppDispatcher.handleAction({
            type: ActionTypes.RECEIVE_CLUSTER,
            slug: slug,
            cluster: cluster
        });
    }
};
