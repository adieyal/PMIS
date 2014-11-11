var React = require("react");
var c3 = require("c3");
var d3 = require("d3");

var Performance = React.createClass({
	componentDidMount: function() {
	    var data = this.props.data;
        var node = this.getDOMNode();

        var chart = c3.generate({
            bindto: node,
            padding: {
                top: 30
            },
            data: {
                columns: data,
                type: 'bar'
            },
            bar: {
                width: '50%'
            }
        });

        var svg = d3.select(node).select('svg');

        svg.append('text')
            .attr("x", 60)
            .attr("y", 45)
            .style("text-anchor", "left")
            .text(this.props.title);
    },
    render: function() {
        return <div className="chart performance">
        </div>;
    }
});
module.exports = Performance;
