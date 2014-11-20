var _ = require('lodash');
var EventEmitter = require('events').EventEmitter;
var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');
var AuthStore = require('./AuthStore');
var DistrictStore = require('./DistrictStore');
var WebAPIUtils = require('./WebAPIUtils');

var CHANGE_EVENT = 'change';

var stores = {};
var state = {};

var ClusterStore = function (slug) {
    var store = stores[slug];

    if (typeof store == 'undefined') {
        store = _.merge({}, EventEmitter.prototype, {
            slug: slug,
            addChangeListener: function(done) {
                this.on(CHANGE_EVENT, done);
            },
            removeChangeListener: function(done) {
                this.removeListener(CHANGE_EVENT, done);
            },
            emitChange: function() {
                this.emit(CHANGE_EVENT);
            },
            getState: function() {
                return state[this.slug];
            }
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
                        store.emitChange();
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
