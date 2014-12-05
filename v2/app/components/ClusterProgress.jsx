var React = require("react");

var Donut = require('./Donut');
var Slider = require('./Slider');

var utils = require('../lib/utils');

var AuthStore = require('../stores/AuthStore');
var ClusterStore = require('../stores/ClusterStore');
var ClusterActions = require('../actions/ClusterActions');

var lists = require('../lib/lists');

var _districtsDomain = [0, 0];

module.exports = React.createClass({
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
            store: this.store ? this.store.getState() : {}
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
	    console.log(store);

        return <div className="cluster-progress">
            <div className="row">
                <div className="ui two column grid">
                    <div className="column">
                        <h2 style={{ marginTop: 0 }}>Big Title</h2>
                        <div className="meta">Year/Year</div>
                    </div>
                    <div className="column">View Reports</div>
                </div>
                <div className="ui six column grid">
                    <div className="column">
                        <Donut data={[]} />
                    </div>
                    <div className="column">
                        <Donut data={[]} />
                    </div>
                    <div className="four wide column">
                        <div className="ui three column grid">
                            <div className="column">
                                One
                            </div>
                            <div className="column">
                                Two
                            </div>
                            <div className="column">
                                Three
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="ui three column grid">
                    <div className="district columnn">District 1</div>
                    <div className="district columnn">District 2</div>
                    <div className="district columnn">District 3</div>
                </div>
            </div>
            <div className="ui two column grid">
                <div className="column">
                    Programmes
                </div>
                <div className="column">
                    Programmes
                </div>
            </div>
        </div>;
    }
});
