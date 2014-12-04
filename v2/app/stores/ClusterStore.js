var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');

var ClusterActions = require('../actions/ClusterActions');

var StoreFactory = require('./StoreFactory');

var AuthStore = require('./AuthStore');
var DistrictStore = require('./DistrictStore');

var stores = {};
var state = {};

var ClusterStore = function (slug) {
    var store = stores[slug];

    if (typeof store == 'undefined') {
        store = StoreFactory(function() {
            this.slug = slug;
            this.getState = function() {
                return state[this.slug];
            };
        });

        store.dispatchToken = AppDispatcher.register(function(payload) {
            var action = payload.action;

            if (action.slug == store.slug) {
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

                        state[action.slug] = action.cluster;
                        store.triggerChange();
                        break;
                    default:
                }
            }
        });

        var remote = require('../lib/remote');
        remote.fetchCluster(slug, AuthStore.getState().auth_token, function(payload) {
            ClusterActions.receiveCluster(slug, payload);
        });

        stores[slug] = store;
    }

    return store;
};

module.exports = ClusterStore;
