var React = require("react");
var c3 = require("c3");
var ActivatorMixin = require('./ActivatorMixin');

var PerformanceChart = {
    create: function (component) {
        var body = component.refs.body.getDOMNode();

        this.chart = c3.generate({
            bindto: body,
            data: {
                columns: [],
                type: 'bar'
            },
            padding: {
                left: 40
            },
            bar: {
                width: '20%'
            },
            color: {
                pattern: [
                    "#37557A",
                    "#AB2C3A"
                ]
            },
            size: {
                height: 130
            }
        });

        this.update(component);
    },

    update: function(component) {
        this.chart.load({
            columns: component.props.data,
            type: 'bar'
        });
    },

    destroy: function () {
    }
};

var Performance = React.createClass({
    mixins: [ ActivatorMixin(PerformanceChart) ],

    render: function() {
        return <div className="widget performance">
            <div className="title">{this.props.title}</div>
            <div ref="body" className="body" />
        </div>;
    }
});
module.exports = Performance;
