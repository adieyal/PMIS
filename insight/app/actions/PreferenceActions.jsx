var AppDispatcher = require('../lib/dispatcher');
var ActionTypes = require('../lib/constants').ActionTypes;

module.exports = {
    setDate: function(year, month) {
        AppDispatcher.handleAction({
            type: ActionTypes.SET_DATE,
            year: year,
            month: month
        });
    }
};
