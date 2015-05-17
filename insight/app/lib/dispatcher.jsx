var Dispatcher = require('flux').Dispatcher;
var utils = require('./utils');

module.exports = utils.extend(new Dispatcher(), {
    handleAction: function (action) {
        console.log('<Dispatcher>', action.type);
        // console.log('<Dispatcher>', JSON.stringify(action));

        this.dispatch({
            action: action
        });
    }
});
