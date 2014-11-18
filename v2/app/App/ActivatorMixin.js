var ActivatorMixin = function (chart) {
    return {
        componentDidMount: function() {
            chart.create(this);
        },
        componentDidUpdate: function() {
            chart.update(this);
        },
        componentWillUnmount: function() {
            chart.destroy(this);
        }
    };
};
module.exports = ActivatorMixin;
