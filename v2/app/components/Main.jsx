var React = require('react');

var Header = require("./Header");
var Footer = require("./Footer");
var Dashboard = require("./Dashboard");
var LoginForm = require("./LoginForm");

var StoreMixin = require('../mixins/StoreMixin');
var AuthStore = require('../stores/AuthStore');
var NotificationStore = require('../stores/NotificationStore');

require('../css/roboto.css');
require('../../node_modules/humane-js/themes/libnotify.css');
require('../../bower_components/semantic-ui/dist/semantic.css');
require('../styles/screen.css');

if (typeof window !== 'undefined') {
    console.log('here');
    window.jQuery = require('../../bower_components/jquery/dist/jquery.js');
    require('../../bower_components/semantic-ui/dist/semantic.js');

    jQuery.fn.api.settings.api = {
        search: BACKEND + '/reports/search?query={query}',
        cluster: BACKEND + '/reports/project/department-of-{slug}/latest/'
    };
}

NotificationStore.addChangeListener(function() {
    var notification = NotificationStore.getLastNotification();

    var humane = require('humane-js');
    var notify = humane.create();

    notify.log(notification);
});

module.exports = React.createClass({
    mixins: [ StoreMixin(AuthStore, 'auth') ],

    getDefaultProps: function () {
        return {
        };
    },

    getInitialState: function () {
        return {
            view: 'dashboard',
            auth: AuthStore.getState(),
            clusters: [
                { slug: "education", view: "index" },
                { slug: "health", view: "index" },
                { slug: "social-development", view: "index" },
                { slug: "culture-sports-science-and-recreation", view: "index" },
                { slug: "community-safety-security-and-liaison", view: "index" },
                { slug: "economic-development-environment-and-tourism", view: "index" }
            ]
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
                content = <Dashboard clusters={this.state.clusters} />;
                break;
        }

        return <div className={ "app " + auth.status }>
            <Header auth={auth} />
            <div className="content">{content}</div>
            <Footer />
        </div>;
    }
});
