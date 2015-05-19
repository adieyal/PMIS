var component = require('../lib/component');
var React = require('react');

module.exports = React.createClass({
  render: function () {
    var logo = this.props.logo;
    return <header>
      <div className="logo">
          <img src={logo} alt="inSight" />
      </div>
    </header>;
  }
});
