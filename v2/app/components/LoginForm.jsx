var React = require("react");
var AuthActions = require("../actions/AuthActions");

var LoginForm = React.createClass({
    componentDidMount: function() {
        this.refs.username.getDOMNode().focus();
    },
    getInitialState: function() {
        return {
            username: null,
            password: null
        };
    },
    login: function (e) {
        e.preventDefault();

        var username = this.refs.username.getDOMNode().value;
        var password = this.refs.password.getDOMNode().value;

        var remote = require('../lib/remote');
        remote.login(username, password, function(data) {
            AuthActions.login(data.auth_token);
        });
    },
    render: function() {
        var errors = this.props.errors || {};

        var nonFieldErrors = '';

        if (errors.non_field_errors) {
            nonFieldErrors = <ul className="errors">
                {errors.non_field_errors.map(function(e, i) {
                    return <div key={i} className="error">{e}</div>;
                })}
            </ul>;
        }

        return <form className="login" onSubmit={this.login}>
            <h3>Login</h3>

            {nonFieldErrors}

            <div className="field">
                <input type="text" ref="username" tabIndex="0" placeholder="Username" />
                { errors.username ? <div className="error">{errors.username}</div> : '' }
            </div>

            <div className="field">
                <input type="password" ref="password" tabIndex="1" placeholder="Password" />
                { errors.password ? <div className="error">{errors.password}</div> : '' }
            </div>

            <button className="btn btn-primary" type="submit" tabIndex="2" onClick={this.login}>Login</button>
        </form>;
    }
});

module.exports = LoginForm;
