var React = require("react");

var Header = require("./Header");
var Dashboard = require("./Dashboard");
var AuthStore = require("./AuthStore");
var StoreMixin = require("./StoreMixin");
var LoginForm = require("./LoginForm");

require("./Notification");

var App = React.createClass({
    mixins: [StoreMixin(AuthStore, 'auth')],
    getInitialState: function () {
        return {
            auth: AuthStore.getState()
        };
    },
	render: function () {
	    require('./roboto.css');
	    require('../../node_modules/c3/c3.css');
	    require('../styles/screen.css');

	    var logo = null;
	    var auth = this.state.auth;

        if (auth.status == 'logged-in') {
            return <div className="app logged-in">
                <Header logo={logo} />
                <Dashboard />
            </div>;
        } else {
            return <div className="app logged-out">
                <LoginForm errors={auth.data} />
            </div>
        }
	}
});
module.exports = App;