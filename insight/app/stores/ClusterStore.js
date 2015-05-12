var utils = require('../lib/utils');

var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

var ClusterActions = require('../actions/ClusterActions');

var StoreFactory = require('./StoreFactory');

var AuthStore = require('./AuthStore');
var DistrictStore = require('./DistrictStore');
var PreferenceStore = require('./PreferenceStore');

var state = {
    clusters: []
};

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
            case ActionTypes.SET_DATE:
                state.clusters = [];
                ClusterStore.triggerChange();
                var preference = PreferenceStore.getState();
                remote.fetchClusters(clusters, AuthStore.getState().authToken, { year: preference.year, month: preference.month });
                break;
            case ActionTypes.RECEIVE_CLUSTER:
                // Force the district store first so it calculates the domain
                // of the districts map coloration correctly first
                AppDispatcher.waitFor([
                    DistrictStore.dispatchToken,
                    PreferenceStore.dispatchToken
                ]);

                state.clusters.push({
                    slug: action.slug,
                    data: action.cluster
                });

                if (state.length < clusters.length) {
                    // Trigger change anyway since we want to show a loader with number of clusters loaded
                } else if(state.length == clusters.length) {
                    // Reorder them according to the cluster property, we've got them all now
                    state.clusters = clusters.map(function(cluster, index) {
                        var stateCluster = utils.find(state, function(stateCluster) {
                            return stateCluster.slug == cluster.slug;
                        });
                        stateCluster.view = cluster.view;
                        return stateCluster;
                    });
                }

                ClusterStore.triggerChange();

                break;
            default:
        }
    });

    if (typeof window != 'undefined') {
        var preference = PreferenceStore.getState();
        var remote = require('../lib/remote');
        var query = { year: preference.year, month: preference.month };
        remote.fetchClusters(clusters, AuthStore.getState().authToken, query);
    }

    return ClusterStore;
};
