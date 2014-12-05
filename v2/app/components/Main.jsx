var React = require('react');

var StoreMixin = require('../mixins/StoreMixin');
var ClusterStore = require("../stores/ClusterStore");

var App = require('./App');

var logo = require('../images/insight.png');

var clusters = [
    { slug: "education", view: "performance" },
    { slug: "health", view: "performance" },
    { slug: "social-development", view: "performance" },
    { slug: "culture-sports-science-and-recreation", view: "performance" },
    { slug: "community-safety-security-and-liaison", view: "performance" },
    { slug: "economic-development-environment-and-tourism", view: "performance" }
];

module.exports = React.createClass({
    mixins: [ StoreMixin(ClusterStore(clusters), 'clusters') ],
    
    getInitialState: function() {
        return {
            clusters: []
        };
    },

    render: function () {
        if (this.state.clusters.length == 0) {
            return <div>Loading...</div>;
        } else {
            return <App logo={logo} clusters={this.state.clusters} />;
        }
    }
});
