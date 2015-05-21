var component = require('../lib/component');
var React = require("react");
var lists = require('../lib/lists');

module.exports = component('Legend', function(props) {
    var length = props.data.length;

    var phases = props.data.map(function (datum, index) {
        var phase = datum[0];
        var value = datum[1];

        var rectX = 0;
        var rectY = index * 35 - 18 * length;

        var textNudge = value > 9 ? 25 : 20;

        var withBlocks = typeof props.withBlocks == 'undefined' ? false : this.props.withBlocks;
        var colours = this.props.colours || 'colours';
        var colour = withBlocks ? lists[colours][index] : "transparent";

        var textProps = {};

        if (withBlocks) {
            textProps.fill = '#ffffff';
        } else {
            textProps.fill = '#000000';
        }

        return <g key={phase}>
            <rect x={rectX} y={rectY} width="30" height="30" fill={colour} />
            <text x={rectX+textNudge} y={rectY+20} textAnchor="end" {...textProps}>{value}</text>
            <text x={rectX+38} y={rectY+20}>{phase}</text>
        </g>;
    }.bind(this));

    var style = {};

    if (props.height) {
        style.height = props.height;
    }

    if (props.width) {
        style.width = props.width;
    }

    return <div className="legend">
        <svg width="100%" style={style} version="1.1" viewBox="0 -160 135 320" preserveAspectRatio="xMidYMid meet">
            {phases}
        </svg>
    </div>;
});
