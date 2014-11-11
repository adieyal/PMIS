var Reflux = require("reflux");
Reflux.nextTick(process.nextTick);

var React = require("react");

// Basic styling
require("./style.scss");

// Init relevant modules
// With a pages/router init only relevant modules for this page.
require("App/init");

// render top-level react component
var App = require("App");
var Main = React.createClass({
	render: function() {
		return <App />;
	}
});
module.exports = Main;
