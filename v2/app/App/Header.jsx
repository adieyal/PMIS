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
        return <header>
            <div className="logo">
                <h1><span className="alt">in</span>Sight</h1>
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
