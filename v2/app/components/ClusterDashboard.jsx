var React = require("react");

var Donut = require('react-proxy!./Donut');
var Slider = require('react-proxy!./Slider');
var Map = require('react-proxy!./Map');

var ProgrammeRow = require('react-proxy!./ProgrammeRow');
var DistrictRow = require('react-proxy!./DistrictRow');

var lists = require('../lib/lists');
var utils = require('../lib/utils');

var AuthStore = require('../stores/AuthStore');
var ClusterStore = require('../stores/ClusterStore');
var ClusterActions = require('../actions/ClusterActions');

var _districtsDomain = [0, 0];

var currentRequest = null;

var ClusterDashboard = React.createClass({
    componentDidMount: function() {
        this.state.view = this.props.view;

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
            view: 'index',
            store: {},
            filtering: false,
            filteredProgrammes: []
        };
    },
    showIndex: function() {
        this.setState({ view: 'index' });
    },
    showProgrammes: function() {
        this.setState({ view: 'programmes' });
    },
    showDistricts: function() {
        this.setState({ view: 'districts' });
    },
    showPlanning: function() {
        this.setState({ view: 'planning' });
    },
    showImplementation: function() {
        this.setState({ view: 'implementation' });
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
    filterProgrammes: function() {
        var query = this.refs.query.getDOMNode().value;

        if(query) {
            this.setState({
                filtering: true,
                filteredProgrammes: []
            });

            var re = new RegExp(query, 'i');

            this.setState({
                filteredProgrammes: this.state.store.programmes.filter(function (p) {
                    return re.test(p.title);
                })
            });
        } else {
            this.setState({
                filtering: false,
                filteredProgrammes: []
            });
        }
    },
    generateProgrammes: function(programmes) {
        var store = this.state.store;

        data = programmes.map(function(p) {
            var numbers = {
                implementation: p.projects.implementation,
                projects: p.projects.total
            };

            var projects = utils.map(Object.keys(lists.projectPhases), function(phase) {
                return [ lists.projectPhases[phase], p.projects[phase] ];
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
            var title = lists.districts[slug];

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
    generatePlanningDonut: function() {
        var store = this.state.store;
        var data = Object.keys(lists.planningPhases).map(function(phase) {
            return [ lists.planningPhases[phase], store['planning-phases'][phase] ];
        });
        return data;
    },
    generateImplementationDonut: function() {
        var store = this.state.store;
        var data = Object.keys(lists.implementationGroups).map(function(groupId) {
            return [ lists.implementationGroups[groupId], store['implementation-groups'][groupId] ];
        });
        return data;
    },
    generateProjectsDonut: function() {
        var store = this.state.store;
        var data = Object.keys(lists.projectPhases).map(function(phase) {
            return [ lists.projectPhases[phase], store[phase + '-projects-total'] ];
        });
        return data;
    },
	render: function() {
	    var store = this.state.store;

	    if (store.client) {
            var view;
            var client = store.client.replace(/^Department of /, '');

            switch (this.state.view) {
            case 'index':
                var domain = utils.flatten(utils.values(_districtsDomain));

                view = <div className="index ui fluid card">
                    <div className="content">
                        <div className="header">{client}</div>
                    </div>

                    <div className="extra content">
                        <div className="ui three column grid slider-row">
                            <div className="column">
                                <div className="header">Total</div>
                                <Slider key="total" data={store['total-slider']} />
                            </div>

                            <div className="planning-column column" onClick={this.showPlanning}>
                                <div className="header">Planning</div>
                                <Slider key="planning" data={store['planning-slider']} />
                            </div>

                            <div className="implementation-column column" onClick={this.showImplementation}>
                                <div className="header">Implementation</div>
                                <Slider key="implementation" data={store['implementation-slider']} />
                            </div>
                        </div>
                    </div>

                    <div className="extra content">
                        <div className="header">Projects</div>
                        <Donut title={store['planning-projects-total'] + ' Projects'} data={this.generateProjectsDonut()} />
                    </div>

                    <div className="extra content">
                        <div className="header">Districts</div>
                        <Map districts={store.districts} domain={domain} onClick={this.showDistricts} height="155" />
                    </div>

                    <div className="extra content">
                        <a className="projects left floated">{store['total-projects']} projects</a>
                        <a className="programmes right floated" onClick={this.showProgrammes}>{store['total-programmes']} programmes</a>
                    </div>
                </div>;
                break
            case 'programmes':
                var programmes = this.state.filtering ? this.state.filteredProgrammes : this.state.store.programmes;

                var programmes = this.generateProgrammes(programmes).map(function(p) {
                    return <ProgrammeRow key={p.title} programme={p} />;
                });

                view = <div className="index ui fluid card">
                    <div className="content">
                        <div className="back-to-cluster header" onClick={this.showIndex}>{client}</div>
                    </div>
                    <div className="programme-rows extra content">
                        {programmes}
                    </div>
                </div>;
                break;
            case 'districts':
                var districts = this.generateDistricts().map(function(d) {
                    return <div className="extra content">
                        <DistrictRow key={d.slug} district={d} />
                    </div>;
                });

                view = <div className="index ui fluid card">
                    <div className="content">
                        <div className="back-to-cluster header" onClick={this.showIndex}>{client}</div>
                    </div>
                    <div className="district-rows extra content">
                        {districts}
                    </div>
                </div>;
                break;
            case 'planning':
                view = <div className="index ui fluid card">
                    <div className="content">
                        <div className="back-to-cluster header" onClick={this.showIndex}>{client}</div>
                    </div>
                    <div className="planning-rows extra content">
                        <div className="header">{store['planning-projects-total']} Projects in Planning</div>
                        <Donut data={this.generatePlanningDonut()} height="240" />
                        <Slider title="Planning" data={store['planning-slider']} height="155" />
                    </div>
                </div>;
                break;
            case 'implementation':
                view = <div className="index ui fluid card">
                    <div className="content">
                        <div className="back-to-cluster header" onClick={this.showIndex}>{client}</div>
                    </div>
                    <div className="implementation-rows extra content">
                        <div className="header">{store['implementation-projects-total']} Projects in Implementation</div>
                        <Donut data={this.generateImplementationDonut()} height="240" />
                        <Slider title="Implementation" data={store['implementation-slider']} height="155" />
                    </div>
                </div>; break;
            }

            return <div className="cluster-dashboard">{view}</div>;
        } else {
            return <div className="cluster-dashboard ui segment">
                <div className="ui active dimmer">
                    <div className="ui text loader">Loading</div>
                </div>
            </div>;
        }
	}
});

module.exports = ClusterDashboard;
