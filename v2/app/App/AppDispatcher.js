var Dispatcher = require('flux').Dispatcher;
var _ = require('lodash');

module.exports = _.extend(new Dispatcher(), {
    handleAction: function (action) {
        console.log(action);

        this.dispatch({
            action: action
        });
    }
});
