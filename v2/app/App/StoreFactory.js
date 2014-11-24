var utils = require('./utils');
var MicroEvent = require('microevent');
var Constants = require('./Constants');

var eventProperties = {
    addChangeListener: function(done) {
        this.bind(Constants.CHANGE_EVENT, done);
    },
    removeChangeListener: function(done) {
        this.unbind(Constants.CHANGE_EVENT, done);
    },
    triggerChange: function() {
        this.trigger(Constants.CHANGE_EVENT);
    }
};

var StoreFactory = function (Constructor) {
    MicroEvent.mixin(Constructor);
    Constructor.prototype = utils.extend(Constructor.prototype, eventProperties);
    return new Constructor();
};

module.exports = StoreFactory;
