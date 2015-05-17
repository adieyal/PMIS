var component = require('omniscient').withDefaults({ jsx: true });
component.debug();

var React = require('react/addons');
var lists = require('../lib/lists');
var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");
var Template = require("./Template");

var NotificationStore = require('../stores/NotificationStore');

var PreferenceActions = require('../actions/PreferenceActions');

var ClusterProgress = require("./ClusterProgress");
var ClusterPerformance = require("./ClusterPerformance");
var ClusterProjects = require("./ClusterProjects");

if (typeof window != 'undefined') {
    /** This can only be done in the browser */
    jQuery = require('jquery');

    require('jquery-address');

    require('semantic-ui');
    require('../styles/screen.css');

    /** How to get to the backend */
    jQuery.fn.api.settings.api = {
        search: BACKEND + '/reports/search?query={query}',
        cluster: BACKEND + '/reports/project/department-of-{slug}/latest/'
    };

    var humane = require('humane-js');

    NotificationStore.addChangeListener(function() {
        var notification = NotificationStore.getLastNotification();
        var notify = humane.create();
        notify.log(notification);
    });

    jQuery.QueryString = (function(a) {
        if (a == "") return {};
        var b = {};

        for (var i = 0; i < a.length; ++i) {
            var p=a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }

        return b;
    })(window.location.search.substr(1).split('&'));
}

var AddressState = {
    getInitialState: function() {
        return {
            clusterId: lists.clusters[0].slug
        };
    },
    componentDidMount: function() {
        if(typeof window != 'undefined') {
            jQuery.address.change(function (evt) {
                this.changeAddress(evt.path);
            }.bind(this));
        }
    },
    changeAddress: function(path) {
        if (this.isMounted()) {
            var state = {
                clusterId: lists.clusters[0].slug
            };

            var parts = path.split('/').slice(1);

            if (parts.length > 0) {
                PreferenceActions.setPreference('view', parts[0] || 'dashboard');
            }

            if (parts.length > 1) {
                state.clusterId = parts[1] || lists.clusters[0].slug;
            }

            if (parts.length > 2) {
                state.programme = parts[2];
            }

            this.setState(state);
        }
    }
};

module.exports = component('App', AddressState,
    function({ logo, view, auth, preference, clusters, projects }) {
        var content;

        switch(view) {
            case 'login':
                content = <LoginForm auth={auth} />;
                break;
            case 'dashboard':
                content = <Dashboard clusters={clusters} />;
                break;
            case 'progress':
                content = <ClusterProgress clusters={clusters} />;
                break;
            case 'performance':
                content = <ClusterPerformance clusters={clusters} />;
                break;
            case 'projects':
                content = <ClusterProjects
                    clusterId={this.state.clusterId}
                    programme={this.state.programme}
                    projects={projects} />;
                break;
        }

        return <Template
            logo={logo}
            auth={auth}
            preference={preference}>
            {content}
        </Template>;
    }
);
