var React = require('react');

var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");
var Template = require("./Template");

var StoreMixin = require('../mixins/StoreMixin');
var AuthStore = require('../stores/AuthStore');
var ClusterStore = require("../stores/ClusterStore");

// var ClusterProgress = require("./ClusterProgress");
var NotificationStore = require('../stores/NotificationStore');

require('../css/roboto.css');
require('../../node_modules/humane-js/themes/libnotify.css');
require('../../bower_components/semantic-ui/dist/semantic.css');
require('../styles/screen.css');

if (typeof window !== 'undefined') {
    var humane = require('humane-js');
    window.jQuery = require('../../bower_components/jquery/dist/jquery.js');
    require('../../bower_components/semantic-ui/dist/semantic.js');

    window.jQuery.fn.api.settings.api = {
        search: BACKEND + '/reports/search?query={query}',
        cluster: BACKEND + '/reports/project/department-of-{slug}/latest/'
    };

    NotificationStore.addChangeListener(function() {
        var notification = NotificationStore.getLastNotification();
        var notify = humane.create();
        notify.log(notification);
    });
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
