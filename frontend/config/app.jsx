/** @jsx React.DOM */

var React = require("react");
var Application = require("../app/" + __resourceQuery.substr(1));

React.render(<Application />, document.body);
