var component = require('../lib/component');
var React = require("react/addons");
var Donut = require('./Donut');
var Slider = require('./Slider');
var DistrictRow = require('./DistrictRow');

var utils = require('../lib/utils');
var lists = require('../lib/lists');

var ClusterActions = require('../actions/ClusterActions');

var methods = {
    mixins: [React.addons.LinkedStateMixin],
    getInitialState: function() {
        return {
            clusterId: lists.clusters[0].slug
        };
    }
};

module.exports = component('ClusterProgress', methods, function({ clusters }) {
    var cluster = clusters.cursor(this.state.clusterId);

    var generateProgrammes = function() {
        data = cluster.get('programmes').map(function(p) {
            var numbers = {
                planning: p.projects.planning,
                implementation: p.projects.implementation
            };

            var planning = utils.map(Object.keys(lists.planningPhases), function(phase) {
                return [ lists.planningPhases[phase], p.planning[phase] ];
            });

            var implementation = utils.map(Object.keys(lists.implementationGroups), function(groupId) {
                return [ lists.implementationGroups[groupId], p.implementation[groupId] ];
            });

            return {
                id: p.id,
                title: p.title,
                numbers: numbers,
                planning: planning,
                implementation: implementation,
                performance: p.performance
            };
        }.bind(this));
        return data;
    };

    var generateDistricts = function() {
        var districts = [];
        var clusterDistricts = cluster.get('districts').toObject();

        for (var slug in clusterDistricts) {
            var districtData = clusterDistricts[slug];
            var title = lists.districts[slug];

            var district = {
                slug: slug,
                title: title,
                numbers: {
                    implementation: districtData.get('projects-implementation')
                },
                performance: districtData.get('performance')
            };

            district.summary = Object.keys(lists.districtSummaryGroups).map(function(groupId) {
                return [ lists.districtSummaryGroups[groupId],
                            districtData.get('summary').get(groupId) ];
            });

            districts.push(district);
        }

        return districts;
    };

    var generateProjectsDonut = function() {
        return Object.keys(lists.projectPhases).map(function(phase) {
            return [ lists.projectPhases[phase],
                    cluster.get(phase + '-projects-total') ];
        });
    };

    var generatePlanningDonut = function() {
        return Object.keys(lists.planningPhases).map(function(phase) {
            return [ lists.planningPhases[phase],
                    cluster.get('planning-phases').get(phase) ];
        });
    };

    var generateImplementationDonut = function() {
        return Object.keys(lists.implementationGroups).map(function(groupId) {
            return [ lists.implementationGroups[groupId],
                    cluster.get('implementation-groups').get(groupId) ];
        });
    };

    var districts = generateDistricts(cluster);
    var programmes = generateProgrammes(cluster);

    return <div className="cluster-progress">
        <div className="ui fluid card">
            <div className="content">
                <h3 className="ui header">
                    <select valueLink={this.linkState('clusterId')}>
                        {utils.map(lists.clusters, function (cluster) {
                            return <option value={cluster.slug}>{cluster.title}</option>;
                        })}
                    </select>
                </h3>
            </div>

            <div className="extra content">
                <div className="ui grid">
                    <div className="two wide column">
                        <Slider title="Planning" data={cluster.get('planning-slider')} height="206" />
                    </div>
                    <div className="two wide column">
                        <Slider title="Implementation" data={cluster.get('implementation-slider')} height="206" />
                    </div>
                    <div className="four wide column">
                        <div className="ui header centered">{cluster.get('total-projects')} Total</div>
                        <Donut data={generateProjectsDonut()} height="206" />
                    </div>
                    <div className="four wide column">
                        <div className="ui header centered">{cluster.get('planning-projects-total')} Planning</div>
                        <Donut data={generatePlanningDonut()} height="206" />
                    </div>
                    <div className="four wide column">
                        <div className="ui header centered">{cluster.get('implementation-projects-total')} Implementation</div>
                        <Donut data={generateImplementationDonut()} height="206" />
                    </div>
                </div>
            </div>
            <div className="extra content">
                <div className="ui grid">
                    <div className="three column row">
                        <div className="column">
                            <DistrictRow district={districts[0]} donut="summary" layout="horizontal" />
                        </div>
                        <div className="column">
                            <DistrictRow district={districts[1]} donut="summary" layout="horizontal" />
                        </div>
                        <div className="column">
                            <DistrictRow district={districts[2]} donut="summary" layout="horizontal" />
                        </div>
                    </div>
                </div>
            </div>
            <div className="extra content">
                <div className="ui grid">
                    <div className="two column row">
                    {programmes.map(function(p) {
                        return <div className="column">
                            <div className="ui fluid card">
                                <div className="content">
                                    <div className="header">{p.title}</div>
                                    <div className="meta">{p.description}</div>
                                </div>
                                <div className="extra content">
                                    <div className="ui three column grid">
                                        <div className="column">
                                            <Donut data={p.planning} height="206" />
                                        </div>
                                        <div className="column">
                                            <Donut data={p.implementation} height="206" />
                                        </div>
                                        <div className="column">
                                            <Slider data={p.performance} height="200" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>;
                    })}
                    </div>
                </div>
            </div>
        </div>
    </div>;
});
