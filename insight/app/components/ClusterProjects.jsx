var component = require('omniscient').withDefaults({ jsx: true });
component.debug();

var React = require('react/addons');
var utils = require('../lib/utils');
var lists = require('../lib/lists');

var projectClasses = {
    'On Target': 'status on-target',
    'Monitor Project': 'status monitor',
    'In danger': 'status in-danger'
};

var methods = {
    mixins: [React.addons.LinkedStateMixin],
    getInitialState: function() {
        return {
            clusterId: this.props.clusterId || lists.clusters[0].slug,
            programme: this.props.programme || '',
            phase: '',
            status: '',
            district: '',
            municipality: '',
            implementing_agent: '',
            sort: 'status',
            direction: 'ascending'
        };
    },
    componentWillReceiveProps: function(props) {
        this.setState({
            clusterId: props.clusterId,
            programme: props.programme
        });
    }
};

module.exports = component('ClusterProjects', methods,
    function({ projects }) {
        var filters = [
            'programme',
            'phase',
            'status',
            'district',
            'municipality',
            'implementing_agent',
        ];
        var filterOptions = {};

        var generateSortClass = (sort) => this.state.sort == sort ? this.state.direction : ''

        var handleSort = function(sort) {
            return function() {
                var direction;

                if (this.state.sort == sort) {
                    direction = this.state.direction == 'ascending' ? 'descending' : 'ascending';
                } else {
                    direction = 'ascending';
                }

                this.setState({
                    sort: sort,
                    direction: direction
                });
            }.bind(this);
        }.bind(this);

        var filterProjects = function(projects) {
            return projects.filter(function (p) {
                var x;
                var allowed = true;

                for(x = 0, l = filters.length; x < l; x++) {
                    var filter = filters[x];
                    if (allowed && this.state[filter]) {
                        if (this.state[filter].toLowerCase() == 'unknown') {
                            allowed = !p.get(filter);
                        } else {
                            allowed = this.state[filter] == p.get(filter);
                        }
                    }
                }

                return allowed;
            }.bind(this));
        }.bind(this);

        var sortProjects = function(projects) {
            return projects.sort(function (a, b) {
                var sort = this.state.sort;
                var directionModifier = this.state.direction == 'ascending' ? 1 : -1;
                var direction;

                if (a.get(sort) > b.get(sort)) {
                    direction = 1;
                } else if (a.get(sort) < b.get(sort)) {
                    direction = -1;
                } else {
                    direction = 0;
                };

                return direction * directionModifier;
            }.bind(this));
        }.bind(this);

        var showProject = function(url) {
            return function() {
                window.location.href = url;
            };
        };

        var clusterProjects = projects.toArray().filter((p) => ('department-of-' + this.state.clusterId) == p.get('cluster'));

        var projects = sortProjects(filterProjects(clusterProjects));

        for(x = 0, l = filters.length; x < l; x++) {
            var filter = filters[x];
            filterOptions[filter] = utils.immUnique(projects, filter, 'Unknown').sort();
        }

        var programmes = utils.map(filterOptions.programme, function(programme) {
            return <option key={programme} value={programme}>{programme}</option>;
        });

        var phases = utils.map(lists.projectPhases, function(title, id) {
            var disabled = !utils.contains(filterOptions.phase, id);
            return <option key={id} value={id} disabled={disabled}>{title}</option>;
        });

        var statuses = utils.map(filterOptions.status, function(status) {
            return <option key={status} value={status}>{status}</option>;
        });

        var districts = utils.map(filterOptions.district, function(district) {
            return <option key={district} value={district}>{district}</option>;
        });

        var municipalities = utils.map(filterOptions.municipality, function(municipality) {
            return <option key={municipality} value={municipality}>{municipality}</option>;
        });

        var implementingAgents = utils.map(filterOptions.implementing_agent, function(implementingAgent) {
            return <option key={implementingAgent} value={implementingAgent}>{implementingAgent}</option>;
        });

        return <div className="cluster-projects">
            <div className="ui fluid card">
                <div className="content">
                    <h3 className="ui header">
                        <select valueLink={this.linkState('clusterId')}>
                            {utils.map(lists.clusters, function (cluster) {
                                return <option key={cluster.slug} value={cluster.slug}>{cluster.title}</option>;
                            })}
                        </select>
                    </h3>
                </div>
                <div className="extra content">
                    <div className="ui form">
                        <div className="fields">
                            <div className="field">
                                <select valueLink={this.linkState('phase')} className="filter filter-phases">
                                    <option key="" value="">All Phases</option>
                                    {phases}
                                </select>
                            </div>
                            <div className="field">
                                <select valueLink={this.linkState('status')} className="filter filter-statuses">
                                    <option key="" value="">All Statuses</option>
                                    {statuses}
                                </select>
                            </div>
                            <div className="field">
                                <select valueLink={this.linkState('programme')} className="filter filter-programmes">
                                    <option key="" value="">All Programmes</option>
                                    {programmes}
                                </select>
                            </div>
                        </div>
                        <div className="fields">
                            <div className="field">
                                <select valueLink={this.linkState('district')} className="filter filter-districts">
                                    <option key="" value="">All Districts</option>
                                    {districts}
                                </select>
                            </div>
                            <div className="field">
                                <select valueLink={this.linkState('municipality')} className="filter filter-municipalities">
                                    <option key="" value="">All Municipalities</option>
                                    {municipalities}
                                </select>
                            </div>
                            <div className="field">
                                <select valueLink={this.linkState('implementing_agent')} className="filter filter-implementing-agents">
                                    <option key="" value="">All Implementing Agents</option>
                                    {implementingAgents}
                                </select>
                            </div>
                            <div className="counts">
                                {projects.length == clusterProjects.size ?
                                    projects.size : (projects.length + ' of ' +
                                                     clusterProjects.length)} projects
                            </div>
                        </div>
                    </div>
                </div>
                <div className="extra content">
                    <table className="ui sortable celled table">
                        <thead>
                            <tr>
                                <th className={generateSortClass('phase')} onClick={handleSort('phase')}>Phase</th>
                                <th className={generateSortClass('status')} onClick={handleSort('status')}>Status</th>
                                <th className={generateSortClass('programme')} onClick={handleSort('programme')}>Programme</th>
                                <th className={generateSortClass('name')} onClick={handleSort('name')}>Name</th>
                                <th className={generateSortClass('district')} onClick={handleSort('district')}>District</th>
                                <th className={generateSortClass('municipality')} onClick={handleSort('municipality')}>Municipality</th>
                                <th className={generateSortClass('implementing_agent')} onClick={handleSort('implementing_agent')}>Implementing Agent</th>
                                <th className={generateSortClass('last_comment')} onClick={handleSort('last_comment')}>Last Comment</th>
                            </tr>
                        </thead>
                        <tbody>
                            {projects.map(function(p) {
                                return <tr key={p.get('id')} className={projectClasses[p.get('status')]}>
                                    <td>{p.get('phase')}</td>
                                    <td>{p.get('status')}</td>
                                    <td className="programme">{p.get('programme')}</td>
                                    <td className="name" onClick={showProject(p.get('url'))}>{p.get('name')}</td> <td>{p.district}</td>
                                    <td>{p.get('municipality')}</td>
                                    <td>{p.get('implementing_agent')}</td>
                                    <td>{p.get('last_comment') ? utils.join(<br />, p.get('last_comment').split('\n')) : ''}</td>
                                </tr>;
                            }.bind(this))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>;
    }
);
