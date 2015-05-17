var component = require('omniscient').withDefaults({ jsx: true });
component.debug();

var React = require("react");

var LoggedOutHeader = require("./LoggedOutHeader");
var LoggedInHeader = require("./LoggedInHeader");

module.exports = component('Header', function(props) {
    if (props.auth.get('status') == 'logged-in') {
        return <LoggedInHeader {...props} />
    } else {
        return <LoggedOutHeader logo={props.logo} />;
    }
});
