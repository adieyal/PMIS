var React = require("react/addons");

var Donut = require('./Donut');
var Slider = require('./Slider');
var DistrictRow = require('./DistrictRow');

var utils = require('../lib/utils');
var lists = require('../lib/lists');

var ClusterActions = require('../actions/ClusterActions');

module.exports = React.createClass({
    mixins: [React.addons.LinkedStateMixin],
    getInitialState: function() {
        return {
            clusterId: lists.clusters[0].slug
        };
    },
    generateProgrammes: function(data) {
        data = data.programmes.map(function(p) {
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
    },
    generateDistricts: function(data) {
        var districts = [];

        for (var slug in data.districts) {
            var districtData = data.districts[slug];
            var title = lists.districts[slug];

            var district = {
                slug: slug,
                title: title,
                numbers: {
                    implementation: districtData['projects-implementation']
                },
                performance: districtData.performance
            };

            district.summary = Object.keys(lists.districtSummaryGroups).map(function(groupId) {
                return [ lists.districtSummaryGroups[groupId], districtData['summary'][groupId] ];
            });

            districts.push(district);
        }

        return districts;
    },
    generateProjectsDonut: function(data) {
        return Object.keys(lists.projectPhases).map(function(phase) {
            return [ lists.projectPhases[phase], data[phase + '-projects-total'] ];
        });
    },
    generatePlanningDonut: function(data) {
        return Object.keys(lists.planningPhases).map(function(phase) {
            return [ lists.planningPhases[phase], data['planning-phases'][phase] ];
        });
    },
    generateImplementationDonut: function(data) {
        return Object.keys(lists.implementationGroups).map(function(groupId) {
            return [ lists.implementationGroups[groupId], data['implementation-groups'][groupId] ];
        });
    },
	render: function() {
	    var cluster = utils.find(this.props.clusters, function(c) {
	        return c.slug == this.state.clusterId;
        }.bind(this));

        var data = cluster.data;

        var client = data.client.replace(/^Department of /, '');

        var districts = this.generateDistricts(data);
        var programmes = this.generateProgrammes(data);

        return <div className="cluster-progress">
            <div className="progress ui fluid card">
                <div className="content">
                    <h2 className="ui header">
                        <select valueLink={this.linkState('clusterId')}>
                            {utils.map(lists.clusters, function (cluster) {
                                return <option value={cluster.slug}>{cluster.title}</option>;
                            })}
                        </select>
                    </h2>
                </div>
                <div className="extra content">
                    <div className="ui grid segment">
                        <div className="two wide column">
                            <Slider title="Planning" data={data['planning-slider']} height="206" />
                        </div>
                        <div className="two wide column">
                            <Slider title="Implementation" data={data['implementation-slider']} height="206" />
                        </div>
                        <div className="four wide column">
                            <div className="ui header centered">{data['total-projects']} Total</div>
                            <Donut data={this.generateProjectsDonut(data)} height="206" />
                        </div>
                        <div className="four wide column">
                            <div className="ui header centered">{data['planning-projects-total']} Planning</div>
                            <Donut data={this.generatePlanningDonut(data)} height="206" />
                        </div>
                        <div className="four wide column">
                            <div className="ui header centered">{data['implementation-projects-total']} Implementation</div>
                            <Donut data={this.generateImplementationDonut(data)} height="206" />
                        </div>
                    </div>
                </div>
                <div className="extra content">
                    <div className="ui grid segment">
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
    }
});
