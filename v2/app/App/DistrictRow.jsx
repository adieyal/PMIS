var React = require("react");

var Pie = require("react-proxy!./Pie");
var Performance = require("react-proxy!./Performance");

var DistrictRow = React.createClass({
	render: function() {
	    var district = this.props.district;
        return <div className="district">
            <div className="row">
                {district.title}
            </div>
            <div className="row">
                <Pie title={district.numbers.implementation + " Projects"} data={district.implementation} />
                <Performance title="Budget" data={district.performance} />
            </div>
        </div>;
	}
});

module.exports = DistrictRow;
