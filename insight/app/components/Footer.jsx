var component = require('../lib/component');
var React = require("react");

var Footer = React.createClass({
    showChangelog: function() {
    },
    render: function() {
        var today = new Date();
        return <footer>
            &copy; {today.getFullYear()} PMIS
        </footer>;
    }
});
module.exports = Footer;
