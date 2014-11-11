var React = require("react");
var Reflux = require("reflux");
var DashboardStore = require("./DashboardStore");
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
            <Performance key="budget" title="Budget" data={this.state.budget} />
            <Performance key="planning" title="Planning" data={this.state.planning} />
            <Performance key="implementation" title="Implementation" data={this.state.implementation} />
        </div>;
	}
});

module.exports = Dashboard;
