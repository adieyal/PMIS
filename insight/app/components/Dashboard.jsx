var React = require("react");

var utils = require('../lib/utils');
var ClusterDashboard = require("./ClusterDashboard");

module.exports = React.createClass({
	render: function() {
        return <div className="ui divided grid">
            <div className="doubling two column row">
                {utils.map(this.props.clusters, function (cluster) {
                    return <div key={cluster.slug} className="column">
                        <ClusterDashboard {...this.props} {...cluster} />
                    </div>;
                }.bind(this))}
            </div>
        </div>;
	}
});
