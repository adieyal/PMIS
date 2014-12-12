var React = require('react/addons');
var utils = require('../lib/utils');
var lists = require('../lib/lists');

module.exports = React.createClass({
    mixins: [React.addons.LinkedStateMixin],
    getInitialState: function() {
        return {
            clusterId: lists.clusters[0].slug,
            phase: '',
            district: '',
            municipality: '',
            sort: 'name',
            direction: 'ascending'
        };
    },
    generateSortClass: function(sort) {
        if (this.state.sort == sort) {
            return this.state.direction;
        }
        return '';
    },
    handleSort: function(sort) {
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
    },
    clusterProjects: function() {
        return this.props.projects.filter(function (p) {
            return ('department-of-' + this.state.clusterId) == p.cluster;
        }.bind(this));
    },
    filterProjects: function(projects) {
        return projects.filter(function (p) {
            var allowed = true;

            if (this.state.phase) {
                if (this.state.phase == 'unknown') {
                    allowed = !p.phase;
                } else {
                    allowed = this.state.phase == p.phase;
                }
            }

            if (allowed && this.state.district) {
                if (this.state.district == 'unknown') {
                    allowed = !p.district;
                } else {
                    allowed = this.state.district == p.district;
                }
            }

            if (allowed && this.state.municipality) {
                if (this.state.municipality == 'unknown') {
                    allowed = !p.municipality;
                } else {
                    allowed = this.state.municipality == p.municipality;
                }
            }

            return allowed;
        }.bind(this));
    },
    sortProjects: function(projects) {
        return projects.sort(function (a, b) {
            var sort = this.state.sort;
            var directionModifier = this.state.direction == 'ascending' ? 1 : -1;
            var direction;

            if (a[sort] > b[sort]) {
                direction = 1;
            } else if (a[sort] < b[sort]) {
                direction = -1;
            } else {
                direction = 0;
            };

            return direction * directionModifier;
        }.bind(this));
    },
    showProject: function(url) {
        return function() {
            window.location.href = url;
        };
    },
    render: function() {
        var clusterProjects = this.clusterProjects();
        var projects = this.sortProjects(this.filterProjects(clusterProjects));

        var projectPhases = utils.unique(projects, 'phase', 'unknown');

        var phases = utils.map(lists.projectPhases, function(title, id) {
            var disabled = !utils.contains(projectPhases, id);
            return <option key={id} value={id} disabled={disabled}>{title}</option>;
        });

        var projectDistricts = utils.unique(projects, 'district', 'Unknown').sort();

        var districts = utils.map(projectDistricts, function(district) {
            return <option key={district} value={district}>{district}</option>;
        });

        var projectMunicipalities = utils.unique(projects, 'municipality', 'Unknown').sort();

        var municipalities = utils.map(projectMunicipalities, function(municipality) {
            return <option key={municipality} value={municipality}>{municipality}</option>;
        });

        return <div className="cluster-projects">
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
                    <div className="ui form">
                        <div className="fields">
                            <div className="field">
                                <select valueLink={this.linkState('phase')} className="filter filter-phases">
                                    <option key="" value="">All Phases</option>
                                    {phases}
                                </select>
                            </div>
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
                            <div className="counts">
                                {projects.length == this.props.projects.length ? this.props.projects.length : (projects.length + ' of ' + clusterProjects.length)} projects
                            </div>
                        </div>
                    </div>
                </div>
                <div className="extra content">
                    <table className="ui sortable celled striped table">
                        <thead>
                            <tr>
                                <th className={this.generateSortClass('phase')} onClick={this.handleSort('phase')}>Phase</th>
                                <th className={this.generateSortClass('status')} onClick={this.handleSort('status')}>Status</th>
                                <th className={this.generateSortClass('name')} onClick={this.handleSort('name')}>Name</th>
                                <th className={this.generateSortClass('district')} onClick={this.handleSort('district')}>District</th>
                                <th className={this.generateSortClass('municipality')} onClick={this.handleSort('municipality')}>Municipality</th>
                                <th className={this.generateSortClass('implementing_agent')} onClick={this.handleSort('implementing_agent')}>Implementing Agent</th>
                                <th className={this.generateSortClass('last_comment')} onClick={this.handleSort('last_comment')}>Last Comment</th>
                            </tr>
                        </thead>
                        <tbody>
                            {projects.map(function(p) {
                                return <tr key={p.id}>
                                    <td>{p.phase}</td>
                                    <td>{p.status}</td>
                                    <td className="name" onClick={this.showProject(p.url)}>{p.name}</td>
                                    <td>{p.district}</td>
                                    <td>{p.municipality}</td>
                                    <td>{p.implementing_agent}</td>
                                    <td>{p.last_comment}</td>
                                </tr>;
                            }.bind(this))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>;
    }
});
