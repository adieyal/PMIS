var React = require("react");
var lists = require('../lib/lists');

module.exports = React.createClass({
    render: function() {
        var needles = [];
        var dataMarkers = [];
        var gradient;

        this.props.data.forEach(function(data, index) {
            var a = Math.PI-Math.PI*(data.position || 0);
            var s = Math.abs(0.5-data.position)*0.28+1;

            var x = Math.cos(a)*57*s;
            var y = 57-Math.sin(a)*57*s;

            var r = 180 * (data.position || 0) - 90;

            var markerProps = {
                transform: 'translate(' + x + ',' + y + ')'
            };

            var needleProps = {
                transform: 'rotate(' + r + ')'
            };

            var rectProps = {
                y: -57 * s,
                height: 57 * s
            };

            var markerInnerProps = {};

            if (data['needle-color']) {
                var gid = 'gauge-needle' + index + '-gradient';
                var color = data['needle-color'];

                gradient = <linearGradient id={gid} x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor={color[1]} />
                    <stop offset="50%" stopColor={color[0]} />
                    <stop offset="100%" stopColor={color[0]} />
                </linearGradient>;

                markerInnerProps.fill = rectProps.fill = 'url(#' + gid + ')';
            }

            var marker;

            switch(data['marker-style']) {
                case 'none':
                    marker = <g {...markerProps} />;
                    break;
                case 'plain':
                default:
                    marker = <g {...markerProps} >
                        <circle className="marker-accent" cx="0" cy="-57" r="6"/>
                        <circle className="marker-outer" cx="0" cy="-57" r="5.5"/>
                        <circle className="marker-inner" cx="0" cy="-57" r="2.5" {...markerInnerProps} />
                        {data.text ? <text className="marker-text" x="0" y="-65" textAnchor="middle">{data.text}</text> : '' }
                    </g>;
                    break;
            }

            var needle;

            switch(data['needle-style']) {
                case 'dashed':
                    needle = <g {...needleProps} className="needle-dashed">
                        <rect className="needle-fill" x="-1.5" width="3" {...rectProps} />
                        <line className="needle-mask" x1="0" y1={-57*s} x2="0" y2="0"/>
                    </g>;
                    break;
                case 'none':
                    needle = <g {...needleProps}/>;
                    break;
                case 'plain':
                default:
                    needle = <g {...needleProps} className="needle-plain">
                        <rect className="needle-fill" x="-1.5" width="3" {...rectProps} />
                    </g>;
            }

            needles.push(needle);
            dataMarkers.push(marker);
        });

        var markers = [];
        for(var x = 0; x <= 20; x++) {
            var degrees = x * 180 / 20;
            var className = (x == 0 ? 'mark-red-main' : (x == 20 ? 'mark-green-main' : 'mark'));
            markers.push(<line className={className} x1="-50" y1="0" x2="-37" y2="0" transform={'rotate(' + degrees + ')'} />);
        }

        var style = this.props.height ? { height: this.props.height } : {};

        return <div className="gauge" style={style}>
            <svg width="100%" height="100%" version="1.1" viewBox="-85 -75 154 90" preserveAspectRatio="xMidYMid meet">
            <defs>
                <linearGradient id="gauge-mark-green-gradient" x1="0" x2="1" y1="0" y2="0">
                    <stop offset="0%" stopColor="#86bf53"/>
                    <stop offset="50%" stopColor="#eceeed"/>
                    <stop offset="100%" stopColor="#eceeed"/>
                </linearGradient>
                <linearGradient id="gauge-mark-red-gradient" x1="1" x2="0" y1="0" y2="0">
                    <stop offset="0%" stopColor="#f0423e"/>
                    <stop offset="50%" stopColor="#eceeed"/>
                    <stop offset="100%" stopColor="#eceeed"/>
                </linearGradient>

                <linearGradient id="gauge-needle-dashed-gradient" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="#b2b4b3"/>
                    <stop offset="100%" stopColor="#eef0ef"/>
                </linearGradient>

                <radialGradient id="gauge-background-gradient" cx="0.5" cy="1" r="0.75">
                    <stop offset="0%" stopColor="#bdbcbc"/>
                    <stop offset="10%" stopColor="#bdbcbc"/>
                    <stop offset="20%" stopColor="#bdbcbc" stopOpacity="0.5"/>
                    <stop offset="30%" stopColor="#bdbcbc" stopOpacity="0.25"/>
                    <stop offset="40%" stopColor="#bdbcbc" stopOpacity="0"/>
                    <stop offset="100%" stopColor="#bdbcbc" stopOpacity="0"/>
                </radialGradient>

                <linearGradient id="gauge-marker-outer-gradient" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="#cccccc"/>
                    <stop offset="100%" stopColor="#ffffff"/>
                </linearGradient>
                <linearGradient id="gauge-marker-outer-stroke-gradient" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="#ffffff"/>
                    <stop offset="100%" stopColor="#b7b9b8"/>
                </linearGradient>
                <linearGradient id="gauge-marker-inner-gradient" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stopColor="#d3d2d2"/>
                    <stop offset="100%" stopColor="#656263"/>
                </linearGradient>

                {gradient}
            </defs>

            <rect className="background" x="-70" y="-115" width="140" height="115"/>

            <g className="markers">
                {markers}
            </g>

            {needles}
            {dataMarkers}

            <g id="gauge-marker-origin">
                <circle className="marker-accent" cx="0" cy="0" r="6"/>
                <circle className="marker-outer" cx="0" cy="0" r="5.5"/>
                <circle className="marker-inner" cx="0" cy="0" r="2.5"/>
            </g>
        </svg>
        </div>;
    }
});
