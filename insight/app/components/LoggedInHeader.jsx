var component = require('../lib/component');
var React = require('react');
var PreferenceActions = require("../actions/PreferenceActions");
var $ = require('jquery');

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

    var onChangeYear = function(e) {
        var financialYear = $(e.target).val();
        PreferenceActions.setFinancialYear(financialYear);
    };

    var financialYear = props.preference.get('year');

    var financialYears = [
        <option key="2013" value="2013">2013/2014</option>,
        <option key="2014" value="2014">2014/2015</option>,
        <option key="2015" value="2015">2015/2016</option>
    ];

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
                    <a ref="logout" className="item" onClick={logout}>Logout</a>
                    <a className="right menu">
                        <div className="item">
                            <div className="ui icon input">
                                <select className="financial-year"
                                onChange={onChangeYear}
                                defaultValue={financialYear}>
                                    {financialYears}
                                </select>
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
