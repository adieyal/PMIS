var React = require('react');

var StoreMixin = require('../mixins/StoreMixin');
var ClusterStore = require("../stores/ClusterStore");
var ProjectStore = require("../stores/ProjectStore");

var App = require('./App');
var lists = require('../lib/lists');

var logo = require('../images/insight.png');

module.exports = React.createClass({
    mixins: [ StoreMixin(ClusterStore(lists.clusters), 'clusterStore'), StoreMixin(ProjectStore, 'projectStore') ],
    
    getInitialState: function() {
        return {
            clusterStore: {
                clusters: []
            },
            projectStore: {
                projects: []
            }
        };
    },

    render: function () {
        var length = this.state.clusterStore.clusters.length;
        if (length < lists.clusters.length) {
            return <div className="ui active inverted dimmer">
                <div className="ui text loader">Loaded {length} clusters</div>
            </div>;
        } else {
            return <App logo={logo} clusters={this.state.clusterStore.clusters} projects={this.state.projectStore.projects} />;
        }
    }
});