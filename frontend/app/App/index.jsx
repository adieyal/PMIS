/** @jsx React.DOM */

var React = require("react");

var Dashboard = require("./Dashboard");

var App = React.createClass({
	render: function() {
	    require('./style.scss');

		return <div className="app">
			<Dashboard />
		</div>;
	}
});
module.exports = App;
