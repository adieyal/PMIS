var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;
var Immutable = require('immutable');

module.exports = {
    setFinancialYear: function (year) {
        AppDispatcher.handleAction(Immutable.fromJS({
            type: ActionTypes.SET_FINANCIAL_YEAR,
            year: year
        }));
    },
    receiveProjects: function (projects) {
        AppDispatcher.handleAction(Immutable.fromJS({
            type: ActionTypes.RECEIVE_PROJECTS,
            projects: projects
        }));
    }
};
