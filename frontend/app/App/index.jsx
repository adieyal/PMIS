/** @jsx React.DOM */

var React = require("react");

var Dashboard = require("./Dashboard");

var App = React.createClass({
	render: function() {
	    require('../../node_modules/c3/c3.css')
	    require('./stylesheets/screen.css');

		return <div className="app">
			<Dashboard />
		</div>;
	}
});
module.exports = App;
