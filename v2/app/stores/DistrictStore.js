var AppDispatcher = require('../lib/dispatcher');
var Constants = require('../lib/constants');
var utils = require('../lib/utils');
var StoreFactory = require('./StoreFactory');

var state = {
    maxProjects: 0,
    districtsByCluster: {}
};

var DistrictStore = StoreFactory(function() {
    this.getState = function() {
        return state;
    };
});

DistrictStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    switch(action.type) {
        case ActionTypes.RECEIVE_CLUSTER:
            if (typeof state.districtsByCluster[action.slug] == 'undefined') {
                state.districtsByCluster[action.slug] = action.cluster.districts;

                previousMaxProjects = state.maxProjects;
                var districts = utils.flatten(utils.map(state.districtsByCluster, function(districts) {
                    return utils.values(districts);
                }));

                var otherMaxProjects = utils.max(utils.pluck(districts, 'projects-implementation'));
                state.maxProjects = Math.max(state.maxProjects, otherMaxProjects);

                if (state.maxProjects > previousMaxProjects) {
                    DistrictStore.triggerChange();
                }
            }
            break;
        default:
    }
});

module.exports = DistrictStore;
