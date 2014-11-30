var React = require("react");

var StoreMixin = require("../mixins/StoreMixin");
var AuthStore = require("../stores/AuthStore");

var Header = require("./Header");
var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");

var NotificationStore = require('../stores/NotificationStore');

require('../css/roboto.css');
require('../../node_modules/humane-js/themes/libnotify.css');
require('../styles/screen.css');

NotificationStore.addChangeListener(function() {
    var notification = NotificationStore.getLastNotification();

    var humane = require('humane-js');
    var notify = humane.create();

    notify.log(notification);
});

var App = React.createClass({
    mixins: [StoreMixin(AuthStore, 'auth')],
    getInitialState: function () {
        return {
            auth: AuthStore.getState()
        };
    },
	render: function () {
	    var logo = null;
	    var auth = this.state.auth;

        if(auth.status == 'logged-in') {
            return <div className="app logged-in">
                <Header logo={logo} />
                <Dashboard />
            </div>;
        } else {
            return <div className="app logged-out">
                <LoginForm errors={auth.data} />
            </div>;
        }
    }
});
module.exports = App;
