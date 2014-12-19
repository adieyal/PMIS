var React = require("react");
var ActivatorMixin = require('../mixins/ActivatorMixin');
var lists = require('../lib/lists');

module.exports = React.createClass({
    render: function() {
        var length = this.props.data.length;

        var phases = this.props.data.map(function (datum, index) {
            var phase = datum[0];
            var value = datum[1];

            var colour = lists.colours[index];

            var rectX = 0;
            var rectY = index * 35 - 18 * length;

            var textNudge = value > 9 ? 25 : 20;

            var withBlocks = typeof this.props.withBlocks == 'undefined' ? false : this.props.withBlocks;

            var textProps = {};

            if (withBlocks) {
                textProps.fill = '#ffffff';
            } else {
                textProps.fill = '#000000';
            }

            return <g key={phase}>
                {withBlocks ? <rect x={rectX} y={rectY} width="30" height="30" fill={colour} /> : ''}
                <text x={rectX+textNudge} y={rectY+20} textAnchor="end" {...textProps}>{value}</text>
                <text x={rectX+38} y={rectY+20}>{phase}</text>
            </g>;
        }.bind(this));

        var style = {};

        if (this.props.height) {
            style.height = this.props.height;
        }

        if (this.props.width) {
            style.width = this.props.width;
        }

        return <div className="legend" style={style}>
            <svg width="100%" height="100%" version="1.1" viewBox="0 -135 135 255" preserveAspectRatio="xMidYMid meet">
                {phases}
            </svg>
        </div>;
    }
});
