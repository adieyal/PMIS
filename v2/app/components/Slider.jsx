'use strict';

var React = require("react");

var Slider = React.createClass({
    styles: {
        long: {
            rect: { width: 3, height: 18 },
            markerText: { x: 4, y: 34 },
            valueText: { x: 4, y: 40 }
        },
        short: {
            rect: { width: 3, height: 8 },
            markerText: { x: 4, y: 22 },
            valueText: { x: 4, y: 28 }
        },
    },

    generateGradient: function (id, color) {
        var gradient = <linearGradient key={id} id={id} x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity="0.1"/>
            <stop offset="100%" stopColor={color}/>
        </linearGradient>;
        return gradient;
    },

    render: function() {
        var gradients = [];
        var markers = [];
        var bars = [];
        var px = 0;

        var aspect = (parseFloat(this.props.aspect) || 1) * 90;

        if (typeof this.props.data != 'undefined') {
            this.props.data.forEach(function (data, i) {
                var x = (aspect - 4) * (data['position'] || 0);
                var transform = 'translate(' + x + ', 0)';

                var style = this.styles[data['marker-style'] || 'short'];

                var markerAccentStyle = data['marker-color'] ? { stroke: data['marker-color'] } : {};

                var markerId = 'marker' + i;
                gradients.push(this.generateGradient(markerId, data['marker-color']));

                var markerStyle = data['marker-color'] ? { stroke: data['marker-color'], fill: 'url(#' + markerId + ')' } : {};

                var barId = 'bar' + i;
                gradients.push(this.generateGradient(barId, data['bar-color']));

                var barStyle = data['bar-color'] ? { stroke: data['bar-color'], fill: 'url(#' + barId + ')' } : {};

                markers.push(<g key={'marker-' + data['marker-text']} id={markerId} transform={transform}>
                    <rect style={markerAccentStyle} className="marker-accent marker-tab" x="2.5" y="8" rx="1" ry="1" width={style.rect.width} height={style.rect.height}/>
                    <circle style={markerAccentStyle} className="marker-accent" cx="4" cy="8" r="4"/>
                    <circle className="marker-outer" cx="4" cy="8" r="3.6"/>
                    <circle style={markerStyle} className="marker-inner" cx="4" cy="8" r="1.75"/>
                    { data['marker-text'] ? <text className="marker-text" x={style.markerText.x} y={style.markerText.y} textAnchor="middle">{ data['marker-text'] }</text> : '' }
                    { data['value-text'] ? <text className="value-text" x={style.valueText.x} y={style.valueText.y} textAnchor="middle">{ data['value-text'] }</text> : '' }
                </g>);

                bars.push(<rect key={'bar-' + data['marker-text']} id={barId} style={barStyle} className="inner-bar" x={px + 4} y="6" rx="2" ry="2" width={x - px} height="4"/>);

                px = x;
            }.bind(this));
        }

        var style = this.props.height ? { height: this.props.height } : {};
        var title = <text x="45" y="-5" textAnchor="middle">{this.props.title || ''}</text>;

        return <div className="slider" style={style} onClick={this.props.onClick}>
            <svg width="100%" height="100%" version="1.1" viewBox="-10 -10 110 50" preserveAspectRatio="xMidYMid meet">

                <defs ref="defs">
                    <linearGradient key="inner-gradient" id="inner-gradient" x1="0" x2="0" y1="0" y2="1">
                        <stop offset="0%" stopColor="#b1b3b2"/>
                        <stop offset="100%" stopColor="#eceeed"/>
                    </linearGradient>
                    <linearGradient key="inner-stroke-gradient" id="inner-stroke-gradient" x1="0" x2="0" y1="0" y2="1">
                        <stop offset="0%" stopColor="#cfd0d0"/>
                        <stop offset="100%" stopColor="#999c9c"/>
                    </linearGradient>
                    <linearGradient key="marker-outer-gradient" id="marker-outer-gradient" x1="0" x2="0" y1="0" y2="1">
                        <stop offset="0%" stopColor="#cccccc"/>
                        <stop offset="100%" stopColor="#ffffff"/>
                    </linearGradient>
                    <linearGradient key="marker-outer-stroke-gradient" id="marker-outer-stroke-gradient" x1="0" x2="0" y1="0" y2="1">
                        <stop offset="0%" stopColor="#ffffff"/>
                        <stop offset="100%" stopColor="#b7b9b8"/>
                    </linearGradient>
                    <linearGradient key="marker-inner-gradient" id="marker-inner-gradient" x1="0" x2="0" y1="0" y2="1">
                        <stop offset="0%" stopColor="#d3d2d2"/>
                        <stop offset="100%" stopColor="#656263"/>
                    </linearGradient>
                    <linearGradient key="marker-tab-gradient" id="marker-tab-gradient" x1="0" x2="0" y1="0" y2="1">
                        <stop offset="0%" stopColor="#b1b3b2"/>
                        <stop offset="100%" stopColor="#eef0ef"/>
                    </linearGradient>

                    {gradients}
                </defs>

                <rect className="outer-bar" width={aspect} x="2" y="4" rx="4" ry="4" height="8"/>
                <rect className="inner-bar" width={aspect-4} x="4" y="6" rx="2" ry="2" height="4"/>

                {title}
                {bars}
                {markers}
            </svg>
        </div>;
    }
});

module.exports = Slider;
