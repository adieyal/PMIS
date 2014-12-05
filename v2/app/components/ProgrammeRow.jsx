var React = require("react");

var Donut = require("./Donut");
var Slider = require("./Slider");

var ProgrammeRow = React.createClass({
	render: function() {
	    var programme = this.props.programme;

        return <div className="programme-row">
            <div className="ui header">{programme.title}</div>
            <div className="extra content">
                <div className="ui two column grid">
                    <div className="column">
                        <Slider height="125" data={programme.performance} />
                    </div>
                    <div className="column">
                        <Donut height="155" title={programme.numbers.implementation + "/" + programme.numbers.projects + " Projects"} data={programme.projects} />
                    </div>
                </div>
            </div>
        </div>;
	}
});

module.exports = ProgrammeRow;
