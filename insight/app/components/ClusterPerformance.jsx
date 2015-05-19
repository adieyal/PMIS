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

module.exports = component('ClusterPerformance', methods, function ({ clusters }) {
    var cluster = clusters.cursor(this.state.clusterId);

    var generateProjectsDonut = function() {
        return Object.keys(lists.projectPhases).map(function(phase) {
            return [ lists.projectPhases[phase], cluster.get(phase + '-projects-total') ];
        });
    };

    var renderExpenditureDiff = function(budget, actual) {
        budget = budget || 0;
        actual = actual || 0;
        var diff = budget - actual;
        var diffType = (diff > 0) ? 'Underexpenditure' : 'Overexpenditure';
        return 'Total ' + diffType + ': ' + utils.toMoney(Math.abs(diff));
    };

    var renderProgramme = function(phase) {
        return function(p) {
            return <div key={p.get('title')} className="eight wide column">
                <h4 className="ui header">{p.get('title')}</h4>
                <div className="ui grid">
                    <div className="eight wide column">
                        <div>Total Projects: {p.get('projects').get(phase)}</div>
                        {phase == 'implementation' ? <div>Total Progress: {p.get('progress')}</div> : ''}
                        <div>Total Budget: {utils.toMoney(p.get('budget'))}</div>
                        <div>{renderExpenditureDiff(p.get('budget'), p.get('expenditure'))}</div>
                    </div>
                    <div className="eight wide column">
                        <Slider data={p.get('performance')} height="120" />
                    </div>
                </div>
            </div>;
        }.bind(this);
    };

    var planningProgrammes = cluster.get('programmes').toArray().filter(function(p) {
        return p.get('projects').get('planning') > 0;
    });

    var implementationProgrammes = cluster.get('programmes').toArray().filter(function(p) {
        return p.get('projects').get('implementation') > 0;
    });

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
                    <div className="four wide column">
                        <h4 className="ui header">
                            Total Projects: {cluster.get('total-projects')}<br />
                            Total Progress: {cluster.get('total-progress')}
                        </h4>
                    </div>
                    <div className="center aligned six wide column">
                        <h4 className="ui header">Total Budget:
                            {utils.toMoney(cluster.get('total-budget'))}</h4>
                        <Donut data={generateProjectsDonut()} height="220" />
                    </div>
                    <div className="center aligned six wide column">
                        <h4 className="ui header">
                            {renderExpenditureDiff(cluster.get('total-budget'), cluster.get('total-expenditure'))}
                        </h4>
                        <Slider data={cluster.get('total-slider')} height="190" />
                    </div>
                </div>
            </div>

            <div className="extra content">
                <div className="ui grid">
                    <div className="four wide column">
                        <h3 className="ui header">Planning</h3>
                        <div>Total Projects: {cluster.get('planning-projects-total')}</div>
                        <div>Total Budget: {utils.toMoney(cluster.get('planning-budget'))}</div>
                        <div>{renderExpenditureDiff(cluster.get('planning-budget'),
                                                         cluster.get('planning-expenditure'))}</div>
                    </div>
                    <div className="four wide column">
                        <Slider data={cluster.get('planning-slider')} height="190" />
                    </div>
                    <div className="four wide column">
                        <h3 className="ui header">Implementation</h3>
                        <div>Total Projects: {cluster.get('implementation-projects-total')}</div>
                        <div>Total Budget: {utils.toMoney(cluster.get('implementation-budget'))}</div>
                        <div>{renderExpenditureDiff(cluster.get('implementation-budget'),
                                                    cluster.get('implementation-expenditure'))}</div>
                    </div>
                    <div className="four wide column">
                        <Slider data={cluster.get('implementation-slider')} height="190" />
                    </div>
                </div>
            </div>

            <div className="extra content">
                <h3 className="ui header" style={{ marginBottom: 20 }}>
                    Planning Programmes
                </h3>

                <div className="ui grid">
                    {planningProgrammes.map(renderProgramme('planning'))}
                </div>
            </div>

            <div className="extra content">
                <h3 className="ui header" style={{ marginBottom: 20 }}>
                    Implementation Programmes
                </h3>

                <div className="ui grid">
                    {implementationProgrammes.map(renderProgramme('implementation'))}
                </div>
            </div>
        </div>
    </div>;
});
