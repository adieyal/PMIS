var React = require('react');

var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");
var Template = require("./Template");

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
                content = <ClusterProgress clusters={this.props.clusters} />;
                break;
        }

        return <Template logo={this.props.logo} auth={auth} view={this.state.view} onSetView={this.setView}>
            {content}
        </Template>;
    }
});
