var React = require("react");

// render top-level react component
var App = require("App");
var Main = React.createClass({
	render: function() {
		return <App />;
	}
});
module.exports = Main;
