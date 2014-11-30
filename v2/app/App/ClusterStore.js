var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');
var AuthStore = require('./AuthStore');
var DistrictStore = require('./DistrictStore');
var StoreFactory = require('./StoreFactory');

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

        stores[slug] = store;
    }

    return store;
};

module.exports = ClusterStore;
