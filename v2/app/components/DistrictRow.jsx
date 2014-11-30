var React = require("react");

var Donut = require("react-proxy!./Donut");
var Slider = require("react-proxy!./Slider");

var DistrictRow = React.createClass({
	render: function() {
	    var district = this.props.district;
        return <div className="district">
            <div className="row">
                {district.title}
            </div>
            <div className="row">
                <Donut height="150" title={district.numbers.implementation + " Projects"} data={district.implementation} />
                <Slider height="150" title="Budget" data={district.performance} />
            </div>
        </div>;
	}
});

module.exports = DistrictRow;
