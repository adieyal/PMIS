var ActivatorMixin = function (thing) {
    return {
        componentDidMount: function() {
            thing.create(this);
        },
        componentDidUpdate: function() {
            thing.update(this);
        },
        componentWillUnmount: function() {
            thing.destroy(this);
        }
    };
};
module.exports = ActivatorMixin;
