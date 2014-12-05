var React = require("react");

var Donut = require("./Donut");
var Slider = require("./Slider");

var DistrictRow = React.createClass({
	render: function() {
	    var district = this.props.district;
        return <div className="district-row">
            <div className="header">{district.title}</div>
            <div className="meta">{district.numbers.implementation} Projects in Implementation</div>
            <div className="ui two column grid">
                <div className="column">
                    <Slider data={district.performance} height="170" />
                </div>
                <div className="column">
                    <Donut data={district.implementation} height="200" />
                </div>
            </div>
        </div>;
    }
});

module.exports = DistrictRow;
