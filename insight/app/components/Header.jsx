var component = require('../lib/component');
var React = require("react");
var LoggedOutHeader = require("./LoggedOutHeader");
var LoggedInHeader = require("./LoggedInHeader");

var logo = require('../images/insight.png');

module.exports = component('Header', function(props) {
    if (props.auth.get('status') == 'logged-in') {
        return <LoggedInHeader logo={logo} {...props} />
    } else {
        return <LoggedOutHeader logo={logo} />;
    }
});
