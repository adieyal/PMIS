var React = require("react");

var Donut = require("react-proxy!./Donut");
var Slider = require("react-proxy!./Slider");

var ProgrammeRow = React.createClass({
	render: function() {
	    var programme = this.props.programme;

        return <div className="programme">
            <div className="row">
                {programme.title}
            </div>
            <div className="row">
                <Donut height="155" title={programme.numbers.implementation + "/" + programme.numbers.projects + " Projects"} data={programme.projects} />
                <Slider height="155" title="Budget" data={programme.performance} />
            </div>
        </div>;
	}
});

module.exports = ProgrammeRow;
