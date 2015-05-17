var React = require("react");
var Slider = require('./Slider');
var utils = require("../lib/utils");

var MetaSlider = React.createClass({
    propTypes: {
        year: React.PropTypes.number.isRequired,
        budget: React.PropTypes.number.isRequired,
        planned: React.PropTypes.number.isRequired,
        actual: React.PropTypes.number.isRequired
    },
    render: function() {
        var ouPercentage = (this.props.planned - this.props.actual)
            / this.props.planned * 100;

        var ouDirection = this.props.actual < this.props.planned ?
            'under' : 'over';

        var adjustment = 0.8;

        var markers = [
            {
                title: 'Actual',
                position: this.props.actual / this.props.budget * adjustment
            },
            {
                title: 'Planned',
                position: this.props.planned / this.props.budget * adjustment
            },
            {
                title: 'Budget',
                position: 1 * adjustment
            }
        ];

        var markerWidth = 2;
        var markerHeight = 20;

        var offsetY = 20;

        return <div className="meta-slider">
            <svg width="100%" height="200" viewBox="0 0 200 200">
                {utils.timesMap(21, function(i) {
                    return <rect
                        x={i * 10 - markerWidth / 4}
                        y={100/2 - markerHeight * 0.75 + offsetY}
                        width={markerWidth/2}
                        height={markerHeight/2} />;
                })}
                {markers.map(function(m, i) {
                    var textX = m.position * 200 - markerWidth;
                    var textY = (100 / 2 - markerHeight) + 30 + offsetY;
                    var perc = (m.position * 100 / adjustment).toFixed(1);

                    return <g key={m.title}>
                        <text
                            textAnchor="end"
                            x={textX - 30 - markerHeight / 4}
                            y={textY}
                            transform={'rotate(90 ' + textX + ',' + textY + ')'}>
                            {perc}
                        </text>
                        <rect x={m.position * 200 - markerWidth/2}
                            y={100/2 - markerHeight + offsetY}
                            width={markerWidth}
                            height={markerHeight}
                            fill="#ff0000" />
                        <text
                            x={textX}
                            y={textY}
                            transform={'rotate(90 ' + textX + ',' + textY + ')'}>
                            {m.title}
                        </text>
                    </g>
                })}
            </svg>
            <table>
                <tr>
                    <th>Total Budget</th><td>{this.props.budget}</td>
                </tr>
                <tr>
                    <th>Planned</th><td>{this.props.planned}</td>
                </tr>
                <tr>
                    <th>Actual</th><td>{this.props.actual}</td>
                </tr>
                <tr>
                    <th>% Over / Under</th><td>{ouPercentage} {ouDirection}</td>
                </tr>
                <tr>
                    <th>Year</th><td>{this.props.year}</td>
                </tr>
            </table>
        </div>;
    }
});

module.exports = MetaSlider;
