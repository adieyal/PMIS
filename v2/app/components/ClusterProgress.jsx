var React = require("react");

var Donut = require('./Donut');
var Slider = require('./Slider');
var DistrictRow = require('./DistrictRow');

var utils = require('../lib/utils');

var ClusterActions = require('../actions/ClusterActions');

var lists = require('../lib/lists');

var _districtsDomain = [0, 0];

module.exports = React.createClass({
    getInitialState: function() {
        return {
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
    generateDistricts: function() {
        var data = this.props.data;
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

        console.log(districts);

        return districts;
    },
    generateProjectsDonut: function() {
        var data = this.props.data;
        return Object.keys(lists.projectPhases).map(function(phase) {
            return [ lists.projectPhases[phase], data[phase + '-projects-total'] ];
        });
    },
    generatePlanningDonut: function() {
        var data = this.props.data;
        return Object.keys(lists.planningPhases).map(function(phase) {
            return [ lists.planningPhases[phase], data['planning-phases'][phase] ];
        });
    },
    generateImplementationDonut: function() {
        var data = this.props.data;
        return Object.keys(lists.implementationGroups).map(function(groupId) {
            return [ lists.implementationGroups[groupId], data['implementation-groups'][groupId] ];
        });
    },
	render: function() {
        var data = this.props.data;
        var client = data.client.replace(/^Department of /, '');
        var districts = this.generateDistricts();

        return <div className="cluster-progress">
            <div className="progress ui fluid card">
                <div className="content">
                    <h2 className="ui header">{client}</h2>
                    <div className="ui floated right">View Reports</div>
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
                            <Donut data={this.generateProjectsDonut()} height="206" />
                        </div>
                        <div className="four wide column">
                            <div className="ui header centered">{data['planning-projects-total']} Planning</div>
                            <Donut data={this.generatePlanningDonut()} height="206" />
                        </div>
                        <div className="four wide column">
                            <div className="ui header centered">{data['implementation-projects-total']} Implementation</div>
                            <Donut data={this.generateImplementationDonut()} height="206" />
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

                        <div className="two column row">
                            <div className="column">
                                Programme Block
                            </div>
                            <div className="column">
                                Programme Block
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>;
    }
});
