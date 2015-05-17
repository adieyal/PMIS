var component = require('omniscient').withDefaults({ jsx: true });
component.debug();

var React = require('react');

var AuthActions = require("../actions/AuthActions");
var ClusterActions = require("../actions/ClusterActions");
var ProjectActions = require("../actions/ProjectActions");
var PreferenceActions = require("../actions/PreferenceActions");
var StoreMixin = require('../mixins/StoreMixin');
var PreferenceStore = require('../stores/PreferenceStore');

var methods = {
    getInitialState: function() {
        return {
            loading: false,
            results: []
        };
    },

    componentDidMount: function() {
        jQuery('.ui .search').search({
            type: 'category'
        });
    }
};

module.exports = component('LoggedInHeader', methods, function (props) {
    var logout = function() {
        var remote = require('../lib/remote');
        remote.logout();
    };

    var loadProjectReport = function(projectId) {
        return function() {
            this.setState(this.getInitialState());
            window.open(BACKEND + '/reports/project/' + projectId + '/latest/');
        }.bind(this);
    };

    var generateClasses = function(view) {
        return (view == props.view ? 'active ' : '') + 'item';
    };

    var onChangeMonth = function(e) {
        var date = e.target.value.split('-');
        PreferenceActions.setDate(date[0], date[1]);
    };

    return <header>
        <div className="ui grid">
            <div className="center aligned two wide column">
                <a href="/">
                    <img src={this.props.logo} height="60" />
                </a>
            </div>
            <div className="fourteen wide column">
                <div className="ui huge menu">
                    <a ref="home" className={generateClasses('dashboard')} href="#/"><i className="home icon" /> Home</a>
                    <a className={generateClasses('progress')} href="#/progress">Progress</a>
                    <a ref="performance" className={generateClasses('performance')} href="#/performance">Performance</a>
                    <a ref="projects" className={generateClasses('projects')} href="#/projects">Project list</a>
                    <a ref="logout" className="item" onClick={this.logout}>Logout</a>
                    <a className="right menu">
                        <div className="item">
                            <div className="ui icon input">
                                <input className="month" type="month"
                                defaultValue={props.preference.get('year') + '-'
                                    + props.preference.get('month')} onChange={onChangeMonth} />
                                <i className="calendar icon" />
                            </div>
                        </div>
                        <div className="item search-item">
                            <div className="ui category search">
                                <div className="ui icon input">
                                    <input className="prompt" type="text" placeholder="Search..." />
                                    <i className="search icon" />
                                </div>
                                <div className="results" />
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </header>;
});
