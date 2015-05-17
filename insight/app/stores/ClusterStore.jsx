var immstruct = require('immstruct');
var Immutable = require('immutable');
var utils = require('../lib/utils');

var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

var ClusterActions = require('../actions/ClusterActions');

var StoreFactory = require('./StoreFactory');

var AuthStore = require('./AuthStore');
var DistrictStore = require('./DistrictStore');
var PreferenceStore = require('./PreferenceStore');

var store = immstruct({
    clusters: {}
});

module.exports = function(clusters) {
    store.dispatchToken = AppDispatcher.register(function(payload) {
        var action = payload.action;
        var ActionTypes = Constants.ActionTypes;

        AppDispatcher.waitFor([
            AuthStore.dispatchToken,
            PreferenceStore.dispatchToken
        ]);

        switch(action.type) {
            case ActionTypes.SET_DATE:
                store.cursor('clusters').update(() => {});

                var preference = PreferenceStore.cursor();
                remote.fetchClusters(clusters,
                    AuthStore.cursor().get('authToken'), {
                        year: preference.get('year'),
                        month: preference.get('month')
                    }
                );
                break;
            case ActionTypes.RECEIVE_CLUSTER:
                // Force the district store first so it calculates the domain
                // of the districts map coloration correctly first
                AppDispatcher.waitFor([
                    DistrictStore.dispatchToken
                ]);

                action.cluster.slug = action.slug;
                store.cursor('clusters').update(action.slug, () => Immutable.fromJS(action.cluster));
                break;
            default:
        }
    });

    if (typeof window != 'undefined') {
        var preference = PreferenceStore.cursor();
        var remote = require('../lib/remote');
        var query = {
            year: preference.get('year'),
            month: preference.get('month')
        };
        remote.fetchClusters(clusters, AuthStore.cursor().get('authToken'), query);
    }

    return store;
};
