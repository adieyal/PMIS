var React = require('react');

var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");
var Template = require("./Template");

var StoreMixin = require('../mixins/StoreMixin');
var AuthStore = require('../stores/AuthStore');
var ClusterStore = require("../stores/ClusterStore");

// var ClusterProgress = require("./ClusterProgress");
var NotificationStore = require('../stores/NotificationStore');

var humane = require('humane-js');
require('humane-js/themes/libnotify.css');

NotificationStore.addChangeListener(function() {
    var notification = NotificationStore.getLastNotification();
    var notify = humane.create();
    notify.log(notification);
});

jQuery = require('jquery');

require('semantic-ui/dist/semantic.js');
require('semantic-ui/dist/semantic.css');

require('../styles/screen.css');

jQuery.fn.api.settings.api = {
    search: BACKEND + '/reports/search?query={query}',
    cluster: BACKEND + '/reports/project/department-of-{slug}/latest/'
};

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

    render: function () {
        var auth = this.state.auth;
        var view = auth.status == 'logged-in' ? this.state.view : 'login';
        var content;

        switch(view) {
            case 'login':
                content = <LoginForm auth={auth} />;
                break;
            case 'dashboard':
                content = <Dashboard clusters={this.props.clusters} />;
                break;
            case 'progress':
                // content = <ClusterProgress slug="health" clusters={this.props.clusters} />;
                break;
        }

        return <Template logo={this.props.logo} auth={auth}>
            {content}
        </Template>;
    }
});
