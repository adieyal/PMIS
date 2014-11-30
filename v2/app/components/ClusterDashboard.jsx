var React = require("react");

var Donut = require('react-proxy!./Donut');
var Slider = require('react-proxy!./Slider');
var Map = require('react-proxy!./Map');

var ProgrammeRow = require('react-proxy!./ProgrammeRow');
var DistrictRow = require('react-proxy!./DistrictRow');

var utils = require('../lib/utils');

var AuthStore = require('../stores/AuthStore');
var ClusterStore = require('../stores/ClusterStore');
var ClusterActions = require('../actions/ClusterActions');

var districts = {
    ehlanzeni: 'Ehlanzeni District',
    gertsibande: 'Gert Sibande District',
    nkangala: 'Nkangala District'
};

var projectPhases = {
    'planning': 'Planning',
    'implementation': 'Implementation',
    'completed': 'Completed',
    'final-accounts': 'Final accounts',
};

var _districtsDomain = [0, 0];

var ClusterDashboard = React.createClass({
    componentDidMount: function() {
        this.store = ClusterStore(this.props.slug);
        this.store.addChangeListener(this._handleStoreChange);

        var remote = require('../lib/remote');
        remote.fetchCluster(this.props.slug, AuthStore.getState().auth_token, function(payload) {
            ClusterActions.receiveCluster(this.props.slug, payload);
        }.bind(this));
    },
    componentWillUnmount: function() {
        this.store.removeChangeListener(this._handleStoreChange);
    },
    _handleStoreChange: function() {
        var store = this.store.getState();
        var domain = utils.pluck(store.districts, 'projects-implementation');
        _districtsDomain[1] = Math.max(_districtsDomain[1], utils.max(domain));
        this.setState({ store: store });
    },
    getInitialState: function() {
        return {
            view: 'default',
            store: {}
        };
    },
    showDefault: function() {
        this.setState({ view: 'default' });
    },
    showProgrammes: function() {
        this.setState({ view: 'programmes' });
    },
    showDistricts: function() {
        this.setState({ view: 'districts' });
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
    generateProgrammes: function() {
        var store = this.state.store;

        data = store.programmes.map(function(p) {
            var numbers = {
                projects: p.projects.total,
                implementation: p.projects.implementation
            };

            var projects = utils.map(Object.keys(projectPhases), function(phase) {
                return [ projectPhases[phase], p.projects[phase] ];
            });

            return {
                id: p.id,
                title: p.title,
                numbers: numbers,
                projects: projects,
                performance: p.performance
            };
        }.bind(this));
        return data;
    },
    generateDistricts: function() {
        var store = this.state.store;
        var result = [];

        for (var slug in store.districts) {
            var district = store.districts[slug];
            var title = districts[slug];

            result.push({
                slug: slug,
                title: title,
                numbers: {
                    implementation: district['projects-implementation']
                },
                implementation: [
                    [ '0 - 50%', district['projects-0-50'] ],
                    [ '51 - 75%', district['projects-51-75'] ],
                    [ '76 - 99%', district['projects-76-99'] ],
                    [ '100%', district['projects-100'] ]
                ],
                performance: district.performance
            });
        }
        return result;
    },
    generateProjectsDonut: function() {
        var store = this.state.store;
        var data = Object.keys(projectPhases).map(function(phase) {
            return [ projectPhases[phase], store[phase + '-projects-total'] ];
        });
        return data;
    },
	render: function() {
	    var store = this.state.store;

	    if (store.client) {
            var view;
            var client = store.client.replace(/^Department of /, '');

            switch (this.state.view) {
            case 'default':
                var domain = utils.flatten(utils.values(_districtsDomain));

                view = <div className="default-view inner">
                    <div className="row">
                        <div className="cluster-title">{client}</div>
                        <div className="cluster-projects"><div className="number">{store['total-projects']}</div>Projects</div>
                        <div className="cluster-programmes"><div className="number" onClick={this.showProgrammes}>{store['total-programmes']}</div>Programmes</div>
                    </div>
                    <div className="row">
                        <Slider key="total" title="Total" data={store['total-slider']} />
                        <Slider key="planning" title="Planning" data={store['planning-slider']} />
                        <Slider key="implementation" title="Implementation" data={store['implementation-slider']} />
                    </div>
                    <div className="row">
                        <Donut data={this.generateProjectsDonut()} height="155" />
                        <Map districts={store.districts} domain={domain} onClick={this.showDistricts} height="155" />
                    </div>
                </div>;
                break
            case 'programmes':
                view = <div className="listing-view inner">
                    <div className="row">
                        <div className="cluster-title" onClick={this.showDefault}>{client}</div>
                        <div className="cluster-year">{store.year}</div>
                        <div className="cluster-search"><input ref="search" type="search" /></div>
                    </div>
                    <div className="row rows">
                        {this.generateProgrammes().map(function(p) {
                            return <ProgrammeRow key={p.title} programme={p} />;
                        })}
                    </div>
                </div>;
                break;
            case 'districts':
                view = <div className="listing-view inner">
                    <div className="row">
                        <div className="cluster-title" onClick={this.showDefault}>{client}</div>
                        <div className="cluster-year">{store.year}</div>
                        <div className="cluster-search"><input ref="search" type="search" /></div>
                    </div>
                    <div className="row rows">
                        {this.generateDistricts().map(function(d) {
                            return <DistrictRow key={d.slug} district={d} />;
                        })}
                    </div>
                </div>;
                break;
            }

            return <div className="cluster-dashboard">{view}</div>;
        } else {
            var loader = require('../images/ajax-loader.gif');
            return <div className="cluster-dashboard loading"><img src={loader} /></div>;
        }
	}
});

module.exports = ClusterDashboard;
