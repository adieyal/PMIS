var component = require('../lib/component');
var immstruct = require('immstruct');
var React = require("react");
var utils = require('../lib/utils');
var lists = require('../lib/lists');
var ClusterDashboard = require("./ClusterDashboard");

module.exports = component('Dashboard', function({ clusters, districts }) {
    function wrapMap(index, func) {
        var results = []
        for (x=0, size=index.size; x < size; x++) {
            results.push(func(index.cursor(x), x));
        }
        return results;
    }

    return <div className="ui divided grid">
        <div className="doubling two column row">
            {utils.map(lists.clusters, function(listCluster) {
                var cluster = clusters.cursor(listCluster.slug);
                return <div key={cluster.get('slug')} className="column">
                    <ClusterDashboard cluster={cluster} districts={districts} />
                </div>;
            })}
        </div>
    </div>;
});
