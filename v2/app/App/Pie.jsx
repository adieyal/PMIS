var React = require("react");
var c3 = require("c3");
var ActivatorMixin = require('./ActivatorMixin');

var PieChart = {
    create: function (component) {
        var body = component.refs.body.getDOMNode();

        this.chart = c3.generate({
            bindto: body,
            padding: {
                top: 10,
                left: 10,
                bottom: 20,
                right: 10
            },
            data: {
                columns: [],
                type: 'pie'
            },
            color: {
                pattern: [
                    "#37557A",
                    "#AB2C3A",
                    "#666666",
                    "#969696",
                    "#bdbdbd",
                    "#d9d9d9"
                ]
            },
            legend: {
                position: 'right'
            },
            size: {
                height: 130
            }
        });

        this.update(component);
    },

    update: function(component) {
        /*
        var columns = utils.reject(component.props.data, function(datum) {
            return datum[1] == 0;
        });
        */

        this.chart.load({
            columns: component.props.data,
            type: 'pie'
        });
    },

    destroy: function () {
    }
};

var Pie = React.createClass({
    mixins: [ ActivatorMixin(PieChart) ],

    render: function() {
        return <div className="widget pie">
            <div className="title">{this.props.title}</div>
            <div ref="body" className="body" />
        </div>;
    }
});

module.exports = Pie;
