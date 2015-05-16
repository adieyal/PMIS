var React = require("react");

var Slider = require('./Slider');

var MetaSlider = React.createClass({
    propTypes: {
        budget: React.PropTypes.number.isRequired,
        planned: React.PropTypes.number.isRequired,
        actual: React.PropTypes.number.isRequired
    },
    render: () =>
        <div>
        Hi there
            <div></div>
        </div>
});

module.exports = MetaSlider;
