var React = require("react");

var Donut = require('react-proxy!./Donut');
var Slider = require('react-proxy!./Slider');

var utils = require('../lib/utils');

var AuthStore = require('../stores/AuthStore');
var ClusterStore = require('../stores/ClusterStore');
var ClusterActions = require('../actions/ClusterActions');

var lists = require('../lib/lists');

var _districtsDomain = [0, 0];

var currentRequest = null;

var ClusterDashboard = React.createClass({
    componentDidMount: function() {
        this.store = ClusterStore(this.props.slug);
        this.store.addChangeListener(this._handleStoreChange);
    },
    componentWillUnmount: function() {
        this.store.removeChangeListener(this._handleStoreChange);
    },
    _handleStoreChange: function() {
        this.setState({ store: store });
    },
    getInitialState: function() {
        return {
            store: {}
        };
    },
    translateNumber: function(num) {
        // Strip off locale, if it's there
        if (typeof num == 'string') {
            num = parseInt(num.replace(/[R,]/g, ''))
        }

        // Translate into millions, with fixed decimal point of 2
        return (num / 1000000).toFixed(2);
    },
    extractValue: function(slider, type) {
        var value = slider.filter(function (entry) {
            return entry['marker-text'] == type;
        });
        if (value.length) {
            return this.translateNumber(value[0]['value-text']);
        } else {
            return null;
        }
    },
	render: function() {
	    var store = this.state.store;

	    if (store.client) {
            var client = store.client.replace(/^Department of /, '');
            return <div className="cluster-progress">
                {client}
            </div>;
        } else {
            return <div className="cluster-progress ui segment">
                <div className="ui active dimmer">
                    <div className="ui text loader">Loading</div>
                </div>
            </div>;
        }
	}
});

module.exports = ClusterDashboard;
