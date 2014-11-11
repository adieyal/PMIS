var React = require("react");
var c3 = require("c3");
var d3 = require("d3");

var Pie = React.createClass({
	componentDidMount: function() {
	    var data = this.props.data;
        var node = this.getDOMNode();

        var chart = c3.generate({
            bindto: node,
            padding: {
                top: 40
            },
            data: {
                columns: data,
                type: 'pie'
            },
            legend: {
                position: 'right'
            }
        });

        var svg = d3.select(node).select('svg');

        svg.append('text')
            .attr("x", 60)
            .attr("y", 45)
            .attr('class', 'title')
            .style("text-anchor", "left")
            .text(this.props.title);
    },
    render: function() {
        return <div className="widget pie-container">
            <div className="pie" />
        </div>;
    }
});
module.exports = Pie;
