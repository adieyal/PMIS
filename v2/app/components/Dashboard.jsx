var React = require("react");
var ClusterDashboard = require("react-proxy!./ClusterDashboard");
var StoreMixin = require('../mixins/StoreMixin');
var PreferenceStore = require('../stores/PreferenceStore');

var Dashboard = React.createClass({
    mixins: [ StoreMixin(PreferenceStore, 'preferences') ],
    getInitialState: function() {
        return {
            preferences: PreferenceStore.getState()
        };
    },
	render: function() {
	    var clusters = this.props.clusters.map(function (cluster) {
	        return <ClusterDashboard {...cluster} key={cluster.slug} />
        });

        return <div className="dashboard">{clusters}</div>;
	}
});

module.exports = Dashboard;
