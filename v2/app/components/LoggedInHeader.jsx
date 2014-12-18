var React = require('react');

var AuthActions = require("../actions/AuthActions");

module.exports = React.createClass({
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
    },

    logout: function() {
        var remote = require('../lib/remote');
        remote.logout(function() {
            AuthActions.logout();
        });
    },

    loadProjectReport: function(projectId) {
        return function() {
            this.setState(this.getInitialState());
            window.open(BACKEND + '/reports/project/' + projectId + '/latest/');
        }.bind(this);
    },

    generateClasses: function(view) {
        return (view == this.props.view ? 'active ' : '') + 'item';
    },

    setView: function(view) {
        return function() {
            this.props.onSetView(view);
        }.bind(this);
    },

    render: function() {
        return <header>
            <div className="ui grid">
                <div className="center aligned two wide column">
                    <a href="/">
                        <img src={this.props.logo} height="60" />
                    </a>
                </div>
                <div className="fourteen wide column">
                    <div className="ui huge menu">
                        <a ref="home" className={this.generateClasses('dashboard')} onClick={this.setView('dashboard')}><i className="home icon" /> Home</a>
                        <a className={this.generateClasses('progress')} onClick={this.setView('progress')}>Progress</a>
                        <a ref="performance" className={this.generateClasses('performance')} onClick={this.setView('performance')}>Performance</a>
                        <a ref="projects" className={this.generateClasses('projects')} onClick={this.setView('projects')}>Projects</a>
                        <a ref="logout" className="item" onClick={this.logout}>Logout</a>
                        <a className="right menu">
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
    }
});
