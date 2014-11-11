var React = require("react");
var Reflux = require("reflux");
var DashboardStore = require("./DashboardStore");

var Pie = require('react-proxy!./Pie');
var Performance = require('react-proxy!./Performance');

var Dashboard = React.createClass({
	mixins: [Reflux.ListenerMixin],
	getInitialState: function() {
		return DashboardStore.getData();
	},
	componentDidMount: function() {
		this.listenTo(DashboardStore, this._onChange);
	},
	_onChange: function() {
		this.setState(this.getInitialState());
	},
	render: function() {
        return <div className="dashboard">
            <div className="row">
                <div className="widget performance-container budget">
                    <Performance key="budget" title="Budget" data={this.state.budget} />
                </div>
                <div className="widget performance-container planning">
                    <Performance key="planning" title="Planning" data={this.state.planning} />
                </div>
                <div className="widget performance-container implementation">
                    <Performance key="implementation" title="Implementation" data={this.state.implementation} />
                </div>
            </div>
            <div className="row">
                <div className="widget pie-container">
                    <Pie title="Projects" data={this.state.projects} />
                </div>
                <div className="widget map-container">
                    <div className="map">&nbsp;</div>
                </div>
            </div>
        </div>;
    }
});

module.exports = Dashboard;
