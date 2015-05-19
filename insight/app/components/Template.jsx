var component = require('../lib/component');
var React = require('react');
var Header = require('./Header');
var Footer = require('./Footer');

module.exports = component('Template', (props) =>
    <div className={props.auth.get('status')}>
        <Header {...props} />
        <div className="content">
            {props.children}
        </div>
        <Footer />
    </div>
);
