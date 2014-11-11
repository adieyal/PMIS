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
            <div class="row">
                <Performance key="budget" title="Budget" data={this.state.budget} />
                <Performance key="planning" title="Planning" data={this.state.planning} />
                <Performance key="implementation" title="Implementation" data={this.state.implementation} />
            </div>
            <div class="row">
                <Pie title="Projects" data={this.state.projects} />
                <div className="map">&nbsp;</div>
            </div>
        </div>;
	}
});

module.exports = Dashboard;
