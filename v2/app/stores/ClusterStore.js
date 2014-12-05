var utils = require('../lib/utils');

var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

var ClusterActions = require('../actions/ClusterActions');

var StoreFactory = require('./StoreFactory');

var AuthStore = require('./AuthStore');
var DistrictStore = require('./DistrictStore');

var state = [];

module.exports = function(clusters) {
    var ClusterStore = StoreFactory(function() {
        this.getState = function() {
            return state;
        };
    });

    ClusterStore.dispatchToken = AppDispatcher.register(function(payload) {
        var action = payload.action;
        var ActionTypes = Constants.ActionTypes;

        AppDispatcher.waitFor([
            AuthStore.dispatchToken
        ]);

        switch(action.type) {
            case ActionTypes.RECEIVE_CLUSTER:
                // Force the district store first so it calculates the domain
                // of the districts map coloration correctly first
                AppDispatcher.waitFor([
                    DistrictStore.dispatchToken
                ]);

                state.push({
                    slug: action.slug,
                    data: action.cluster
                });

                // Only trigger change once we've got all the clusters required
                if (state.length == clusters.length) {
                    // But first, reorder them according to the cluster property
                    state = clusters.map(function(cluster, index) {
                        var stateCluster = utils.find(state, function(stateCluster) {
                            return stateCluster.slug == cluster.slug;
                        });
                        stateCluster.view = cluster.view;
                        return stateCluster;
                    });

                    ClusterStore.triggerChange();
                }

                break;
            default:
        }
    });

    if (typeof window != 'undefined') {
        var remote = require('../lib/remote');

        clusters.forEach(function(cluster) {
            remote.fetchCluster(cluster.slug, AuthStore.getState().auth_token, function(payload) {
                ClusterActions.receiveCluster(cluster.slug, payload);
            });
        });
    }

    return ClusterStore;
};
