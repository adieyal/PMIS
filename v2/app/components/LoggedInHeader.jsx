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

    showProgress: function() {
        console.log(this);

        this._owner.setState({ view: 'progress' });
    },

    render: function() {
        return <header>
            <div className="ui menu">
                <a ref="home" className="active item"><i className="home icon" /> Home</a>
                <a className="item" onClick={this.showProgress}>Progress</a>
                <a ref="performance" className="item">Performance</a>
                <a ref="projects" className="item">Projects</a>
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
        </header>;
    }
});
