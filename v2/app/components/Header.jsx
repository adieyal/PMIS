var React = require("react");

var LoggedOutHeader = require("./LoggedOutHeader");
var LoggedInHeader = require("./LoggedInHeader");

var Header = React.createClass({
    render: function() {
        var auth = this.props.auth;
        var logo = this.props.logo;

        if (auth.status == 'logged-in') {
            return <LoggedInHeader logo={this.props.logo} auth={this.props.auth} />;
        } else {
            return <LoggedOutHeader logo={this.props.logo} />;
        }
    }
});

module.exports = Header;
