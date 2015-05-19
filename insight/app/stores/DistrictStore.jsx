'use strict';

var immstruct = require('immstruct');
var Immutable = require('immutable');
var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var utils = require('../lib/utils');
var PreferenceStore = require('./PreferenceStore');

var store = immstruct({
    districts: {},
    maxProjects: 0
});

store.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.get('action');
    var ActionTypes = Constants.ActionTypes;

    AppDispatcher.waitFor([
        PreferenceStore.dispatchToken
    ]);

    switch(action.get('type')) {
        case ActionTypes.RECEIVE_CLUSTER:
            store.cursor().update('districts', function (current) {
                return current.set(action.get('cluster').get('slug'),
                                   action.get('cluster').get('districts').toObject());
            });

            store.cursor().update('maxProjects', () => {
                var clusterDistricts = action.get('cluster').get('districts').toArray();
                var result = clusterDistricts.reduce(function(acc, d) {
                    var projects = d.get('projects-implementation');
                    return Math.max(acc, projects);
                }, store.cursor().get('maxProjects'));
                return result;
            })
            break;
        default:
    }
});

module.exports = store;
