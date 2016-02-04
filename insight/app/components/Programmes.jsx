var component = require('../lib/component');
var React = require('react/addons');
var Donut = require("./Donut");
var Slider = require("./Slider");

module.exports = React.createClass({
    mixins: [ React.addons.LinkedStateMixin ],
    getInitialState: function() {
        return {
            filter: ''
        };
    },
    getProgrammes: function() {
        if (this.state.filter) {
            var re = new RegExp(this.state.filter, 'i');
            return this.props.programmes.filter(function (p) {
                return re.test(p.title);
            });
        } else {
            return this.props.programmes;
        }
    },
    setView: function(programme) {
        return function(phase, status) {
            var href = '/#/projects/' + this.props.clusterId + '/' + programme;

            if (typeof phase != 'undefined') {
                href += '/' + phase;
            }

            if (typeof status != 'undefined') {
                href += '/' + status;
            }

            console.log(href);

            window.location.href = href;
        }.bind(this);
    },
    render: function() {
        var total = this.props.programmes.length;
        var programmes = this.getProgrammes();

        return <div key="programmes" title="Programmes">
            <div className="ui two column grid" style={{ marginBottom: 6 }}>
                <div className="column">
                    <div className="ui icon input">
                        <input ref="filter" type="text" placeholder="Filter programmes" valueLink={this.linkState('filter')} />
                        <i className="search icon" />
                    </div>
                </div>
                <div className="right aligned column">
                    <div className="ui meta">
                        {this.state.filter ? programmes.length + ' of ' + total + ' programmes' : total + ' programmes'}
                    </div>
                </div>
            </div>
            <div className="scrollable programme-rows">
                {programmes.map(function(p) {
                    return <div className="programme-row" onClick={this.setView(p.title)}>
                        <h4 className="ui header">{p.title}</h4>
                        <div className="extra content">
                            <div className="ui two column grid">
                                <div className="column">
                                    <Slider height="100" data={p.performance} />
                                </div>
                                <div className="column">
                                    <Donut height="125"
                                        onClick={this.setView(p.title)}
                                        count={p.numbers.projects}
                                        title={p.numbers.implementation + "/" + p.numbers.projects + " Projects"} data={p.projects} />
                                </div>
                            </div>
                        </div>
                    </div>;
                }.bind(this))}
            </div>
        </div>;
    }
});
