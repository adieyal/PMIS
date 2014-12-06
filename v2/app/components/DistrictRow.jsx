var React = require("react");

var Donut = require("./Donut");
var Slider = require("./Slider");

var DistrictRow = React.createClass({
    render: function() {
        var district = this.props.district;
        return <div className="district-row">
            <div className="ui header">{district.title}</div>
            <div className="meta">{district.numbers.implementation} Projects in Implementation</div>
            <Slider data={district.performance} height="170" />
            <Donut data={district.implementation} height="200" />
        </div>;
    }
});

module.exports = DistrictRow;
