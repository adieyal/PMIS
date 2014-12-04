var React = require('react');

var Header = require('./Header');
var Footer = require('./Footer');

module.exports = React.createClass({
    render: function() {
        var auth = this.props.auth;
        var logo = this.props.logo;

        return <div className={ auth.status }>
            <Header logo={logo} auth={auth} />
            <div className="content">
                {this.props.children}
            </div>
            <Footer />
        </div>;
    }
});
