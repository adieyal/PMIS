var React = require('react');

var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");
var Template = require("./Template");
var ClusterProjects = require("./ClusterProjects");

var StoreMixin = require('../mixins/StoreMixin');
var AuthStore = require('../stores/AuthStore');
var ClusterStore = require("../stores/ClusterStore");

var ClusterProgress = require("./ClusterProgress");
var NotificationStore = require('../stores/NotificationStore');

if (typeof window != 'undefined') {
    /** This can only be done in the browser */
    jQuery = require('jquery');
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
        StoreMixin(AuthStore, 'auth'),
    ],

    getInitialState: function () {
        return {
            view: 'dashboard',
            auth: AuthStore.getState()
        };
    },

    setView: function (view) {
        this.setState({ view: view });
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
                content = <Dashboard clusters={this.props.clusters} />;
                break;
            case 'progress':
                content = <ClusterProgress clusters={this.props.clusters} />;
                break;
            case 'projects':
                content = <ClusterProjects projects={this.props.projects} />;
                break;
        }

        return <Template logo={this.props.logo} auth={auth} view={this.state.view} onSetView={this.setView}>
            {content}
        </Template>;
    }
});
