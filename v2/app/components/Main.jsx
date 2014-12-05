var React = require('react');

var StoreMixin = require('../mixins/StoreMixin');
var ClusterStore = require("../stores/ClusterStore");

var App = require('./App');

require('../../node_modules/humane-js/themes/libnotify.css');
require('../../bower_components/semantic-ui/dist/semantic.css');
require('../styles/screen.css');

if (typeof window !== 'undefined') {
    window.jQuery = require('../../bower_components/jquery/dist/jquery.js');
    require('../../bower_components/semantic-ui/dist/semantic.js');

    window.jQuery.fn.api.settings.api = {
        search: BACKEND + '/reports/search?query={query}',
        cluster: BACKEND + '/reports/project/department-of-{slug}/latest/'
    };
}

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
            return <App logo={this.props.logo} clusters={this.state.clusters} />;
        }
    }
});
