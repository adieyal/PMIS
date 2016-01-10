var component = require('../lib/component');
var React = require("react/addons");

var Gauge = require('./Gauge');
var Donut = require('./Donut');
var Legend = require('./Legend');
var Slider = require('./Slider');
// var MetaSlider = require('./MetaSlider');
var DistrictMap = require('./DistrictMap');

var Tabs = require('./Tabs');

var Programmes = require('./Programmes');
var DistrictRow = require('./DistrictRow');

var lists = require('../lib/lists');
var utils = require('../lib/utils');

var methods = {
    mixins: [React.addons.LinkedStateMixin],
    getInitialState: function() {
        return {
            tab: 'performance',
            performanceTab: 'overview'
        };
    }
};

module.exports = component('ClusterDashboard', methods,
    function ({ cluster, districts }) {
        var changePerformanceTab = (tab) => (e) => {
            e.preventDefault();
            this.setState({
                tab: 'performance',
                performanceTab: tab
            });
        };

        var generateProgrammes = function() {
            var data = cluster.get('programmes').toArray().map(function(p) {
                var projects = p.cursor('projects');

                var numbers = {
                    implementation: projects.get('implementation'),
                    projects: projects.get('total')
                };

                var projects = utils.map(Object.keys(lists.projectPhases), function(phase) {
                    return [ lists.projectPhases[phase],
                            p.get('projects').get(phase) ];
                });

                return {
                    id: p.get('id'),
                    title: p.get('title'),
                    numbers: numbers,
                    projects: projects,
                    performance: p.get('performance')
                };
            }.bind(this));
            return data;
        };

        var generateDistricts = function() {
            var result = [];

            for (var slug in cluster.get('districts').toObject()) {
                var district = cluster.get('districts').get(slug);
                var title = lists.districts[slug];
                var completeness = district.get('completeness');

                result.push({
                    slug: slug,
                    title: title,
                    numbers: {
                        implementation: district.get('projects-implementation')
                    },
                    implementation: [
                        [ '0 - 50%', completeness.get('projects-0-50') ],
                        [ '51 - 75%', completeness.get('projects-51-75') ],
                        [ '76 - 99%', completeness.get('projects-76-99') ],
                        [ '100%', completeness.get('projects-100') ]
                    ],
                    performance: district.get('performance')
                });
            }
            return result;
        };

        var generatePlanningDonut = function() {
            return Object.keys(lists.planningPhases).map(function(phase) {
                return [ lists.planningPhases[phase], cluster.get('planning-phases').get(phase) ];
            });
        };

        var generateImplementationLegend = function() {
            return Object.keys(lists.implementationGroups).map(function(groupId) {
                return [ lists.implementationGroups[groupId], cluster.get('implementation-groups').get(groupId) ];
            });
        };

        var generateProjectsDonut = function() {
            return Object.keys(lists.projectPhases).map(function(phase) {
                return [ lists.projectPhases[phase], cluster.get(phase + '-projects-total') ];
            });
        };

        var listCluster = utils.find(lists.clusters, function(listCluster) {
            return listCluster.slug == cluster.get('slug');
        });

        var domain = [ 0, utils.max(utils.pluck(cluster.get('districts'), 'projects-implementation')) ];

        var implementation = generateImplementationLegend();

        return <div className="cluster-dashboard">
            <div className="index ui fluid card">
                <div className="content">
                    <h2 className="cluster-title ui header"
                    onClick={changePerformanceTab('overview')} style={{
                        backgroundColor: listCluster.colour }}>{listCluster.title}</h2>

                    <Tabs ref="outerTab" state={this.state} attribute="tab">
                        <div key="performance" title="Performance">
                            <Tabs ref="innerTab" type="inner" state={this.state} attribute="performanceTab">
                                <div key="overview" title="Overview">
                                    <div className="ui two column grid slider-row">
                                        <div className="column">
                                            <Slider key="total" data={cluster.get('total-slider')} title="Total" height="120" />
                                        </div>

                                        <div className="planning-column column" onClick={changePerformanceTab('planning')}>
                                            <Slider key="planning" data={cluster.get('planning-slider')} title="Planning" height="120" />
                                        </div>

                                        <div className="implementation-column column" onClick={changePerformanceTab('implementation')}>
                                            <Slider key="implementation"
                                            data={cluster.get('implementation-slider')} title="Implementation" height="120" />
                                        </div>

                                        <div className="gauge-column column">
                                            <Gauge key="gauge" data={cluster.get('total-progress-gauge')} height="110" />
                                        </div>
                                    </div>
                                </div>

                                <div key="projects" title="Projects">
                                    <div className="ui header">{cluster.get('total-projects')} Projects in Total</div>
                                    <div className="ui grid">
                                        <div className="six wide column">
                                            <Slider data={cluster.get('total-slider')} height="190" />
                                        </div>
                                        <div className="ten wide column">
                                            <Donut
                                            count={cluster.get('total-projects')} data={generateProjectsDonut()} height="206" />
                                        </div>
                                    </div>
                                </div>

                                <div key="planning" title="Planning">
                                    <div className="ui header">{cluster.get('planning-projects-total')} Projects in Planning</div>
                                    <div className="ui grid">
                                        <div className="six wide column">
                                            <Slider data={cluster.get('planning-slider')} height="190" />
                                        </div>
                                        <div className="ten wide column">
                                            <Donut
                                                count={cluster.get('planning-projects-total')}
                                                data={generatePlanningDonut()} height="206" />
                                        </div>
                                    </div>
                                </div>

                                <div key="implementation" title="Implementation">
                                    <div className="ui header">{cluster.get('implementation-projects-total')} Projects in Implementation</div>
                                    <div className="ui grid">
                                        <div className="six wide column">
                                            <Slider data={cluster.get('implementation-slider')} height="120" />
                                            <Gauge data={cluster.get('total-progress-gauge')} height="120" />
                                        </div>
                                        <div className="ten wide column">
                                            <Legend data={implementation} height="280" />
                                        </div>
                                    </div>
                                </div>
                            </Tabs>
                        </div>

                        <Programmes key="programmes" title="Programmes" clusterId={cluster.get('slug')} programmes={generateProgrammes()} />

                        <div key="districts" title="Districts">
                            <div className="ui two column grid">
                                <div className="column">
                                    <DistrictMap clusterId={cluster.get('slug')} districts={districts} domain={domain} height="200" />
                                </div>
                                <div className="column scrollable district-rows">
                                {generateDistricts().map(function(d) {
                                    return <div key={d.slug} className="extra content">
                                        <DistrictRow district={d} />
                                    </div>;
                                })}
                                </div>
                            </div>
                        </div>
                    </Tabs>
                </div>
            </div>
        </div>;
    }
);
