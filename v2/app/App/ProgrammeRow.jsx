var React = require("react");

var Pie = require("react-proxy!./Pie");
var Performance = require("react-proxy!./Performance");

var ProgrammeRow = React.createClass({
	render: function() {
	    var programme = this.props.programme;
        return <div className="programme">
            <div className="row">
                {programme.title}
            </div>
            <div className="row">
                <Pie title={programme.numbers.implementation + "/" + programme.numbers.projects + " Projects"} data={programme.projects} />
                <Performance title="Budget" data={programme.performance} />
            </div>
        </div>;
	}
});

module.exports = ProgrammeRow;
