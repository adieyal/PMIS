var Dispatcher = require('flux').Dispatcher;
var utils = require('./utils');
var Immutable = require('immutable');

module.exports = utils.extend(new Dispatcher(), {
    handleAction: function (action) {
        this.dispatch(Immutable.fromJS({
            action: action
        }));
    }
});
