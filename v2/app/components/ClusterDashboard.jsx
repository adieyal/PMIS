var React = require("react/addons");

var Gauge = require('./Gauge');
var Donut = require('./Donut');
var Legend = require('./Legend');
var Slider = require('./Slider');
var DistrictMap = require('./DistrictMap');

var Tabs = require('./Tabs');

var Programmes = require('./Programmes');
var DistrictRow = require('./DistrictRow');

var lists = require('../lib/lists');
var utils = require('../lib/utils');
var count = 0;

module.exports = React.createClass({
    mixins: [React.addons.LinkedStateMixin],
    getInitialState: function() {
        return {
            tab: 'performance',
            performanceTab: 'overview'
        };
    },
    changeTab: function(tab) {
        return function(e) {
            e.preventDefault();
            this.setState({
                tab: tab
            });
        }.bind(this);
    },
    changePerformanceTab: function(tab) {
        return function(e) {
            e.preventDefault();
            this.setState({
                tab: 'performance',
                performanceTab: tab
            });
        }.bind(this);
    },
    generateProgrammes: function() {
        var data = this.props.data.programmes.map(function(p) {
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
        var data = this.props.data;
        var result = [];

        for (var slug in data.districts) {
            var district = data.districts[slug];
            var title = lists.districts[slug];

            result.push({
                slug: slug,
                title: title,
                numbers: {
                    implementation: district['projects-implementation']
                },
                implementation: [
                    [ '0 - 50%', district.completeness['projects-0-50'] ],
                    [ '51 - 75%', district.completeness['projects-51-75'] ],
                    [ '76 - 99%', district.completeness['projects-76-99'] ],
                    [ '100%', district.completeness['projects-100'] ]
                ],
                performance: district.performance
            });
        }
        return result;
    },
    generatePlanningDonut: function() {
        var data = this.props.data;
        return Object.keys(lists.planningPhases).map(function(phase) {
            return [ lists.planningPhases[phase], data['planning-phases'][phase] ];
        });
    },
    generateImplementationLegend: function() {
        var data = this.props.data;
        return Object.keys(lists.implementationGroups).map(function(groupId) {
            return [ lists.implementationGroups[groupId], data['implementation-groups'][groupId] ];
        });
    },
    generateProjectsDonut: function() {
        var data = this.props.data;
        return Object.keys(lists.projectPhases).map(function(phase) {
            return [ lists.projectPhases[phase], data[phase + '-projects-total'] ];
        });
    },
    render: function() {
        var data = this.props.data;
        var client = data.client.replace(/^Department of /, '');
        var domain = [ 0, utils.max(utils.pluck(this.props.data.districts, 'projects-implementation')) ];

        return <div className="cluster-dashboard">
            <div className="index ui fluid card">
                <div className="content">
                    <h2 className="cluster-title ui header" onClick={this.changePerformanceTab('overview')}>{client}</h2>

                    <Tabs ref="outerTab" state={this.state} attribute="tab">
                        <div key="performance" title="Performance">
                            <Tabs ref="innerTab" type="inner" state={this.state} attribute="performanceTab">
                                <div key="overview" title="Overview">
                                    <div className="ui two column grid slider-row">
                                        <div className="column">
                                            <Slider key="total" data={data['total-slider']} title="Total" height="200" />
                                        </div>

                                        <div className="implementation-column column" onClick={this.changePerformanceTab('implementation')}>
                                            <Slider key="implementation" data={data['implementation-slider']} title="Implementation" height="200" />
                                        </div>

                                        <div className="planning-column column" onClick={this.changePerformanceTab('planning')}>
                                            <Slider key="planning" data={data['planning-slider']} title="Planning" height="200" />
                                        </div>

                                        <div className="gauge-column column">
                                            <Gauge key="gauge" data={data['total-progress-gauge']} height="227" />
                                        </div>
                                    </div>
                                </div>

                                <div key="projects" title="Projects">
                                    <div className="ui header">{data['total-projects']} Projects in Total</div>
                                    <div className="ui grid">
                                        <div className="six wide column">
                                            <Slider data={data['total-slider']} height="190" />
                                        </div>
                                        <div className="ten wide column">
                                            <Donut data={this.generateProjectsDonut()} height="206" />
                                        </div>
                                    </div>
                                </div>

                                <div key="planning" title="Planning">
                                    <div className="ui header">{data['planning-projects-total']} Projects in Planning</div>
                                    <div className="ui grid">
                                        <div className="six wide column">
                                            <Slider data={data['planning-slider']} height="190" />
                                        </div>
                                        <div className="ten wide column">
                                            <Donut data={this.generatePlanningDonut()} height="206" />
                                        </div>
                                    </div>
                                </div>

                                <div key="implementation" title="Implementation">
                                    <div className="ui header">{data['implementation-projects-total']} Projects in Implementation</div>
                                    <div className="ui grid">
                                        <div className="six wide column">
                                            <Slider data={data['implementation-slider']} height="190" />
                                            <Gauge data={data['total-progress-gauge']} height="190" />
                                        </div>
                                        <div className="ten wide column">
                                            <Legend data={this.generateImplementationLegend()} height="380" />
                                        </div>
                                    </div>
                                </div>
                            </Tabs>
                        </div>

                        <Programmes key="programmes" title="Programmes" programmes={this.generateProgrammes()} />

                        <div key="districts" title="Districts">
                            <div className="ui two column grid">
                                <div className="column">
                                    <DistrictMap districts={data.districts} domain={domain} height="400" />
                                </div>
                                <div className="column scrollable district-rows">
                                {this.generateDistricts().map(function(d) {
                                    return <div key={d.slug} className="extra content">
                                        <DistrictRow district={d} />
                                    </div>;
                                })}
                                </div>
                            </div>
                        </div>
                    </Tabs>
                </div>

                <div className="extra content">
                    <a className="projects left floated" onClick={this.changePerformanceTab('projects')}>{data['total-projects']} projects</a>
                    <a className="programmes right floated" onClick={this.changeTab('programmes')}>{data['total-programmes']} programmes</a>
                </div>
            </div>
        </div>;
    }
});
