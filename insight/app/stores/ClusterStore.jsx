var immstruct = require('immstruct');
var Immutable = require('immutable');
var lists = require('../lib/lists');

var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

var AuthStore = require('./AuthStore');
var DistrictStore = require('./DistrictStore');
var PreferenceStore = require('./PreferenceStore');

var clusters = lists.clusters;

var store = immstruct({
    clusters: {}
});

store.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.get('action');
    var ActionTypes = Constants.ActionTypes;

    AppDispatcher.waitFor([
        AuthStore.dispatchToken,
        PreferenceStore.dispatchToken
    ]);

    switch(action.get('type')) {
        case ActionTypes.SET_FINANCIAL_YEAR:
            store.cursor('clusters').update(() => Immutable.fromJS({}));

            var preference = PreferenceStore.cursor();
            remote.fetchClusters(clusters,
                                 AuthStore.cursor().get('authToken'),
                                 preference.get('year'));
            break;
        case ActionTypes.RECEIVE_CLUSTER:
            // Force the district store first so it calculates the domain
            // of the districts map coloration correctly first
            AppDispatcher.waitFor([
                DistrictStore.dispatchToken
            ]);

            var cluster = action.get('cluster');
            store.cursor('clusters').set(cluster.get('slug'),
                                         Immutable.fromJS(cluster));
            break;
        default:
    }
});

if (typeof window != 'undefined') {
    var preference = PreferenceStore.cursor();
    var remote = require('../lib/remote');
    remote.fetchClusters(clusters,
                         AuthStore.cursor().get('authToken'),
                         preference.get('year'));
}

module.exports = store;
