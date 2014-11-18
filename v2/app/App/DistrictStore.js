var _ = require('lodash');
var EventEmitter = require('events').EventEmitter;
var AppDispatcher = require('./AppDispatcher');
var Constants = require('./Constants');

var state = {
    maxProjects: 0,
    districtsByCluster: {}
};

var DistrictStore = _.merge({}, EventEmitter.prototype, {
    addChangeListener: function(done) {
        this.on(Constants.CHANGE_EVENT, done);
    },
    removeChangeListener: function(done) {
        this.removeListener(Constants.CHANGE_EVENT, done);
    },
    emitChange: function() {
        this.emit(Constants.CHANGE_EVENT);
    },
    getState: function() {
        return state;
    }
});

DistrictStore.dispatchToken = AppDispatcher.register(function(payload) {
    var action = payload.action;
    var ActionTypes = Constants.ActionTypes;

    switch(action.type) {
        case ActionTypes.RECEIVE_DATA:
            if (typeof state.districtsByCluster[action.slug] == 'undefined') {
                state.districtsByCluster[action.slug] = action.districts;
                previousMaxProjects = state.maxProjects;
                var districts = _.flatten(_.map(state.districtsByCluster), function(districts) {
                    return _.values(districts);
                });
                var otherMaxProjects = _.max(_.pluck(districts, 'projects-implementation'));
                state.maxProjects = Math.max(state.maxProjects, otherMaxProjects);

                if (state.maxProjects > previousMaxProjects) {
                    DistrictStore.emitChange();
                }
            }
            break;
        default:
    }
});

module.exports = DistrictStore;
