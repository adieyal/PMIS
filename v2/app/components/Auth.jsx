var React = require("react");

var StoreMixin = require("../mixins/StoreMixin");
var AuthStore = require("../stores/AuthStore");
var AuthActions = require("../actions/AuthActions");

var Auth = React.createClass({
    mixins: [ StoreMixin(AuthStore) ],
    getInitialState: function() {
        return AuthStore.getState();
    },
    login: function() {
        var username = this.refs.username.getDOMNode().value;
        var password = this.refs.password.getDOMNode().value;
        AuthActions.login(username, password);
    },
    logout: function() {
        AuthActions.logout();
    },
    render: function() {
        if (this.state.username) {
            return <div className="auth">
                Logged in as {this.state.username} <button onClick={this.logout}>Logout</button>
            </div>;
        } else {
            return <div className="auth">
                <form>
                    <input type="text" ref="username" placeholder="Username" />
                    <input type="password" ref="password" placeholder="Password" />
                    <input type="submit" value="Submit" />
                </form>
            </div>;
        }
    }
});

module.exports = Auth;
