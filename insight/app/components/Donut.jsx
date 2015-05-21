// var component = require('../lib/component');
var React = require("react");
var Legend = require('./Legend');
var lists = require('../lib/lists');

var maxArc = 2 * Math.PI - 1e-6;
var arcOffset = - Math.PI / 2;
var innerRadius = 25;
var outerRadius = 65;
var margin = 2 * Math.PI * 1 / 100;

function arc(innerRadius, outerRadius, startAngle, endAngle) {
    var r0 = innerRadius,
        r1 = outerRadius,
        a0 = startAngle + arcOffset,
        a1 = endAngle + arcOffset,
        da = (a1 < a0 && (da = a0, a0 = a1, a1 = da), a1 - a0),
        df = da < Math.PI ? "0" : "1",
        c0 = Math.cos(a0),
        s0 = Math.sin(a0),
        c1 = Math.cos(a1),
        s1 = Math.sin(a1);

    return da >= maxArc ? (r0 ? "M0," + r1 +
        " A" + r1 + "," + r1 + " 0 1,1 0," + (-r1) +
        " A" + r1 + "," + r1 + " 0 1,1 0," + r1 +
        " M0," + r0 +
        " A" + r0 + "," + r0 + " 0 1,0 0," + (-r0) +
        " A" + r0 + "," + r0 + " 0 1,0 0," + r0 +
        " Z" :
        "M0," + r1 +
        " A" + r1 + "," + r1 + " 0 1,1 0," + (-r1) +
        " A" + r1 + "," + r1 + " 0 1,1 0," + r1 +
        " Z") : (r0 ? "M" + r1 * c0 + "," + r1 * s0 +
        " A" + r1 + "," + r1 + " 0 " + df + ",1 " + r1 * c1 + "," + r1 * s1 +
        " L" + r0 * c1 + "," + r0 * s1 +
        " A" + r0 + "," + r0 + " 0 " + df + ",0 " + r0 * c0 + "," + r0 * s0 +
        " Z" : "M" + r1 * c0 + "," + r1 * s0 +
        " A" + r1 + "," + r1 + " 0 " + df + ",1 " + r1 * c1 + "," + r1 * s1 +
        " L0,0" +
        " Z");
}

var Donut = React.createClass({
    render: function() {
        var total = this.props.data.reduce(function (acc, datum) {
            return acc + datum[1];
        }, 0);

        if (total <= 0) {
            return <div className="donut">
                <svg width="100%" height={this.props.height} version="1.1" viewBox="-130 -110 450 220" preserveAspectRatio="xMidYMid meet">
                    <text x="100" y="-10" style={{ fontSize: 40 }} textAnchor="middle">No Data</text>
                </svg>
            </div>;
        }

        var endAngle = 0;

        var length = this.props.data.length;
        var colours = this.props.colours || 'colours';

        var phases = this.props.data.map(function (datum, index) {
            var value = datum[1];

            var percentage = total > 0 ? parseInt(value / total * 100) + '%' : '';

            var startAngle = endAngle;
            var delta = value / total * 2 * Math.PI;
            endAngle = startAngle + delta;

            var thisMargin = length > 1 ? margin : 0;

            var phase = datum[0];
            var colour = lists[colours][index];

            var path;
            if (total > 0) {
                path = <path d={arc(innerRadius, outerRadius, startAngle, endAngle - thisMargin)} fill={colour} />;
            } else {
                path = '';
            }

            var textAngle = (startAngle + endAngle) / 2 + arcOffset;
            var textRadius = outerRadius + 25 + ((textAngle > (Math.PI / 2) && textAngle < (Math.PI * 1.5)) ? 5 : 0);

            var textX = Math.cos(textAngle) * textRadius - ((textAngle > (Math.PI / 2) && textAngle < (Math.PI * 1.5)) ? 15 : 0);
            var textY = Math.sin(textAngle) * textRadius;

            return <g key={phase}>
                <text x={textX} y={textY}>{percentage}</text>
                {path}
            </g>;
        }.bind(this));

        return <div className="donut">
            <div className="ui grid">
                <div className="eight wide column">
                    <svg width="100%" height={this.props.height} version="1.1" viewBox="-105 -145 215 290" preserveAspectRatio="xMidYMid meet">
                        {phases}
                    </svg>
                </div>
                <div className="eight wide column">
                    <Legend height={this.props.height} withBlocks={true} data={this.props.data} colours={colours} />
                </div>
            </div>
        </div>;
    }
});

module.exports = Donut;
