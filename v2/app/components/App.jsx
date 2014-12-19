var React = require('react/addons');

var lists = require('../lib/lists');

var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");
var Template = require("./Template");

var StoreMixin = require('../mixins/StoreMixin');
var AuthStore = require('../stores/AuthStore');
var ClusterStore = require("../stores/ClusterStore");

var ClusterProgress = require("./ClusterProgress");
var ClusterPerformance = require("./ClusterPerformance");
var ClusterProjects = require("./ClusterProjects");

var NotificationStore = require('../stores/NotificationStore');

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

module.exports = React.createClass({
    mixins: [
        React.addons.LinkedStateMixin,
        StoreMixin(AuthStore, 'auth'),
    ],

    getInitialState: function () {
        var path = window.location.hash.replace(/^#/, '');
        var state = this.generatePathState(path);
        state.auth = AuthStore.getState();
        return state;
    },

    setView: function (view) {
        this.setState({ view: view });
    },

    generatePathState: function(path) {
        var state = {
            view: 'dashboard',
            clusterId: lists.clusters[0].slug
        };

        var parts = path.split('/').slice(1);

        if (parts.length > 0) {
            state.view = parts[0] || 'dashboard';
        }

        if (parts.length > 1) {
            state.clusterId = parts[1] || lists.clusters[0].slug;
        }

        if (parts.length > 2) {
            state.programme = parts[2];
        }

        return state;
    },

    changeAddress: function(path) {
        var pathState = this.generatePathState(path);
        this.setState(pathState);
    },

    componentDidMount: function() {
        if(typeof window != 'undefined') {
            jQuery.address.change(function (evt) {
                this.changeAddress(evt.path);
            }.bind(this));
        }
    },

    render: function () {
        var auth = this.state.auth;
        var loggedIn = auth.status == 'logged-in';
        // var loggedIn = (auth.status == 'logged-in' || jQuery.QueryString['authToken'] == 'browserling');
        var view = loggedIn ? this.state.view : 'login';
        var content;

        switch(view) {
            case 'login':
                content = <LoginForm auth={auth} />;
                break;
            case 'dashboard':
                content = <Dashboard appView={this.linkState('view')} clusters={this.props.clusters} />;
                break;
            case 'progress':
                content = <ClusterProgress clusters={this.props.clusters} />;
                break;
            case 'performance':
                content = <ClusterPerformance clusters={this.props.clusters} />;
                break;
            case 'projects':
                content = <ClusterProjects clusterId={this.state.clusterId} programme={this.state.programme} projects={this.props.projects} />;
                break;
        }

        return <Template logo={this.props.logo} auth={auth} view={this.state.view} onSetView={this.setView}>
            {content}
        </Template>;
    }
});
