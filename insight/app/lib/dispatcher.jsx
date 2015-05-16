var Dispatcher = require('flux').Dispatcher;
var utils = require('./utils');

module.exports = utils.extend(new Dispatcher(), {
    handleAction: function (action) {
        // console.log(action);

        this.dispatch({
            action: action
        });
    }
});
