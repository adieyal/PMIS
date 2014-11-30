var React = require("react");
var ActivatorMixin = require('../mixins/ActivatorMixin');

var maxArc = 2 * Math.PI - 1e-6;
var arcOffset = - Math.PI / 2;
var innerRadius = 25;
var outerRadius = 65;
var margin = 2 * Math.PI * 1 / 100;

var phaseColours = {
    Planning: '#1f77b4',
    Implementation: '#ff7f0e',
    Completed: '#2ca02c',
    'Final accounts': '#d62728'
};

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

    return da >= maxArc
      ? (r0
        ? "M0," + r1
        + " A" + r1 + "," + r1 + " 0 1,1 0," + (-r1)
        + " A" + r1 + "," + r1 + " 0 1,1 0," + r1
        + " M0," + r0
        + " A" + r0 + "," + r0 + " 0 1,0 0," + (-r0)
        + " A" + r0 + "," + r0 + " 0 1,0 0," + r0
        + " Z"
        : "M0," + r1
        + " A" + r1 + "," + r1 + " 0 1,1 0," + (-r1)
        + " A" + r1 + "," + r1 + " 0 1,1 0," + r1
        + " Z")
      : (r0
        ? "M" + r1 * c0 + "," + r1 * s0
        + " A" + r1 + "," + r1 + " 0 " + df + ",1 " + r1 * c1 + "," + r1 * s1
        + " L" + r0 * c1 + "," + r0 * s1
        + " A" + r0 + "," + r0 + " 0 " + df + ",0 " + r0 * c0 + "," + r0 * s0
        + " Z"
        : "M" + r1 * c0 + "," + r1 * s0
        + " A" + r1 + "," + r1 + " 0 " + df + ",1 " + r1 * c1 + "," + r1 * s1
        + " L0,0"
        + " Z");
}

var Donut = React.createClass({
    render: function() {
        var total = this.props.data.reduce(function (acc, datum) {
            return acc + datum[1];
        }, 0);

        var is_grey = total == 0;
        var endAngle = 0;

        /*
        var data = this.props.data.filter(function(datum) {
            return datum[1] > 0;
        });
        oconsole.log(data);
        */

        var phases = this.props.data.map(function (datum, index) {
            var value = datum[1];

            var percentage = parseInt(value / total * 100) + '%';

            var startAngle = endAngle;
            var delta = value / total * 2 * Math.PI;
            endAngle = startAngle + delta;

            var thisMargin = this.props.data.length > 1 ? margin : 0;

            var path = arc(innerRadius, outerRadius, startAngle, endAngle - thisMargin);

            var phase = datum[0];
            var colour = phaseColours[phase];

            var rectX = 160;
            var rectY = index * 50 - 100;

            var textAngle = (startAngle + endAngle) / 2 + arcOffset;
            var textRadius = outerRadius + 25 + ((textAngle > (Math.PI / 2) && textAngle < (Math.PI * 1.5)) ? 5 : 0);

            var textX = Math.cos(textAngle) * textRadius - ((textAngle > (Math.PI / 2) && textAngle < (Math.PI * 1.5)) ? 15 : 0);
            var textY = Math.sin(textAngle) * textRadius;

            var textNudge = value > 9 ? 30 : 25;

            var key = this.props.keyPrefix + phase;

            console.log(value);

            return <g key={key}>
                <rect x={rectX} y={rectY} width="40" height="40" fill={colour} />
                <text x={rectX+textNudge} y={rectY+25} fill="#ffffff" textAnchor="end">{value}</text>
                <text x={rectX+48} y={rectY+26}>{phase}</text>
                <text x={textX} y={textY}>{percentage}</text>
                <path d={path} fill={colour} />
            </g>;
        }.bind(this));

        return <div className="widget donut" style={{ height: this.props.height }}>
            <svg width="100%" height="147" version="1.1" viewBox="-130 -80 530 140" preserveAspectRatio="xMidYMid meet">
                {phases}
            </svg>
        </div>;
    }
});

module.exports = Donut;
