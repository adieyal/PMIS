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
        return <div className="dashboard">
            <ClusterDashboard key="education" slug="education" />
            <ClusterDashboard key="health" slug="health" />
            <ClusterDashboard key="sd" slug="social-development" />
            <ClusterDashboard key="cssr" slug="culture-sports-science-and-recreation" />
            <ClusterDashboard key="cssl" slug="community-safety-security-and-liaison" />
            <ClusterDashboard key="edet" slug="economic-development-environment-and-tourism" />
        </div>;
	}
});

module.exports = Dashboard;
