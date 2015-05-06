var React = require("react");
var AuthActions = require("../actions/AuthActions");
var NotificationActions = require("../actions/NotificationActions");
var utils = require('../lib/utils');

module.exports = React.createClass({
    componentDidMount: function() {
        var rules = {
            username: {
                identifier: 'username',
                rules: [{
                    type: 'empty',
                    prompt: 'Enter your username'
                }]
            },
            password: {
                identifier: 'password',
                rules: [{
                    type: 'empty',
                    prompt: 'Enter your password'
                }]
            }
        };

        var $form = window.jQuery('.ui.form', this.getDOMNode());

        window.jQuery('.ui.form', this.getDOMNode()).form(rules, {
            inline: true,
            on: 'blur',
            onSuccess: this.login
        });
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
            AuthActions.login(data.authToken);
        });
    },
    render: function() {
        var auth = this.props.auth;
        var data = auth.data || {};

        var success = Object.keys(data).length === 0;

        var errors;

        if (!success) {
            errors = <ul>{utils.map(data, function(validationErrors) {
                validationErrors.map(function(validationError) {
                    return <li>{validationError}</li>;
                });
            })}</ul>;
        }

        return <div className="ui segment">
            <div className={"login ui form " + (success ? 'success' : 'error') }>
                <h4 className="ui header">Login</h4>

                <div className={"required field" + (data.username ? " error" : "")}>
                    <div className="ui icon input">
                        <input type="text" ref="username" name="username" placeholder="Username" />
                        <i className="user icon" />
                    </div>
                </div>

                <div className={"required field" + (data.password ? " error": "")}>
                    <div className="ui icon input">
                        <input type="password" ref="password" name="password" placeholder="Password" />
                        <i className="lock icon" />
                    </div>
                </div>

                <button className="ui submit button">Login</button>

                <div className="ui error message">{errors}</div>
            </div>
        </div>;
    }
});
