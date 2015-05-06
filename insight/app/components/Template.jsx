var React = require('react');

var Header = require('./Header');
var Footer = require('./Footer');

module.exports = React.createClass({
    render: function() {
        var auth = this.props.auth;

        return <div className={ auth.status }>
            <Header logo={this.props.logo} auth={auth} view={this.props.view} onSetView={this.props.onSetView} />
            <div className="content">
                {this.props.children}
            </div>
            <Footer />
        </div>;
    }
});
