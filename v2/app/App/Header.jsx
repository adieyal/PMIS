var React = require("react");
var WebAPIUtils = require('./WebAPIUtils');
var AuthActions = require("./AuthActions");

var Header = React.createClass({
    logout: function() {
        WebAPIUtils.logout(function() {
            AuthActions.logout();
        });
    },
    render: function() {
        var insight = require('../images/insight.png');

        return <header>
            <div className="logo">
                <img src={insight} alt="inSight" />
            </div>
            <nav className="menu">
                <ul>
                    <li><a href="#">Progress</a></li>
                    <li><a href="#">Performance</a></li>
                    <li><a href="#">Projects</a></li>
                    <li><a href="#" onClick={this.logout}>Logout</a></li>
                </ul>
            </nav>
            <div className="search">
                <input type="search" placeholder="Search here" />
            </div>
        </header>;
    }
});
module.exports = Header;
