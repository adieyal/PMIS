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
    generateProjectsDonut: function() {
	    var cluster = utils.find(this.props.clusters, function(c) {
	        return c.slug == this.state.clusterId;
        }.bind(this));

        var data = cluster.data;

        return Object.keys(lists.projectPhases).map(function(phase) {
            return [ lists.projectPhases[phase], data[phase + '-projects-total'] ];
        });
    },
    renderExpenditureDiff: function(budget, actual) {
        budget = budget || 0;
        actual = actual || 0;
        var diff = budget - actual;
        var diffType = (diff > 0) ? 'Underexpenditure' : 'Overexpenditure';
        return 'Total ' + diffType + ': ' + utils.toMoney(diff);
    },
    renderProgramme: function(phase) {
        return function(p) {
            return <div key={p.title} className="eight wide column">
                <div className="ui header">{p.title}</div>
                <div className="ui grid">
                    <div className="eight wide column">
                        Total Projects: {p.projects[phase]}<br />
                        Total Projects: ??? %<br />
                        Total Budget: {utils.toMoney(p.budget)}<br />
                        {this.renderExpenditureDiff(p.budget, p.expenditure)}
                    </div>
                    <div className="eight wide column">
                        <Slider data={p.performance} height="120" />
                    </div>
                </div>
            </div>;
        }.bind(this);
    },
	render: function() {
	    var cluster = utils.find(this.props.clusters, function(c) {
	        return c.slug == this.state.clusterId;
        }.bind(this));

        var data = cluster.data;

        var planningProgrammes = data.programmes.filter(function(p) {
            return p.projects.planning > 0;
        });

        var implementationProgrammes = data.programmes.filter(function(p) {
            return p.projects.implementation > 0;
        });

        return <div className="cluster-progress">
            <div className="ui fluid card">
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
                    <div className="ui grid">
                        <div className="four wide column">
                            <div className="ui header">
                                Total Projects: {data['total-projects']}
                            </div>
                            <div className="ui header">
                                Total Projects: ??? %
                            </div>
                        </div>
                        <div className="center aligned six wide column">
                            <div className="ui header">Total Budget: {utils.toMoney(data['total-budget'])}</div>
                            <Donut data={this.generateProjectsDonut()} height="206" />
                        </div>
                        <div className="center aligned six wide column">
                            <div className="ui header">{this.renderExpenditureDiff(data['total-budget'], data['total-expenditure'])}</div>
                            <Slider data={data['total-slider']} height="190" />
                        </div>
                    </div>
                </div>

                <div className="extra content">
                    <div className="ui grid">
                        <div className="four wide column">
                            <h1 className="ui header">Planning</h1>
                            <div className="ui header">Total Projects: {data['planning-projects-total']}</div>
                            <div className="ui header">Total Budget: {utils.toMoney(data['planning-budget'])}</div>
                            <div className="ui header">{this.renderExpenditureDiff(data['planning-budget'], data['planning-expenditure'])}</div>
                        </div>
                        <div className="four wide column">
                            <Slider data={data['planning-slider']} height="190" />
                        </div>
                        <div className="four wide column">
                            <h1 className="ui header">Implementation</h1>
                            <div className="ui header">Total Projects: {data['implementation-projects-total']}</div>
                            <div className="ui header">Total Budget: {utils.toMoney(data['implementation-budget'])}</div>
                            <div className="ui header">{this.renderExpenditureDiff(data['implementation-budget'], data['implementation-expenditure'])}</div>
                        </div>
                        <div className="four wide column">
                            <Slider data={data['implementation-slider']} height="190" />
                        </div>
                    </div>
                </div>

                <div className="extra content">
                    <h1 className="ui header" style={{ marginBottom: 20 }}>
                        Planning Programmes
                    </h1>

                    <div className="ui grid">
                        {planningProgrammes.map(this.renderProgramme('planning'))}
                    </div>
                </div>

                <div className="extra content">
                    <h1 className="ui header" style={{ marginBottom: 20 }}>
                        Implementation Programmes
                    </h1>

                    <div className="ui grid">
                        {implementationProgrammes.map(this.renderProgramme('implementation'))}
                    </div>
                </div>
            </div>
        </div>;
    }
});
