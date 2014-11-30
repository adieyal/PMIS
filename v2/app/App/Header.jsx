var React = require("react");
var StoreMixin = require('./StoreMixin');
var AuthStore = require("./AuthStore");
var AuthActions = require("./AuthActions");

var currentRequest;

var Header = React.createClass({
    getInitialState: function() {
        return {
            loading: false,
            results: []
        };
    },
    search: function() {
        this.setState({
            loading: true,
            results: []
        });

        if (currentRequest) {
            currentRequest.abort();
        }

        var WebAPIUtils = require('./WebAPIUtils');

        var query = this.refs.query.getDOMNode().value;

        currentRequest = WebAPIUtils.search(query, AuthStore.getState().auth_token, function(results) {
            this.setState({
                loading: false,
                results: results
            });
        }.bind(this));
    },
    logout: function() {
        var WebAPIUtils = require('./WebAPIUtils');
        WebAPIUtils.logout(function() {
            AuthActions.logout();
        });
    },
    loadProjectReport: function(project_id) {
        return function() {
            this.setState(this.getInitialState());
            window.open(BACKEND + '/reports/project/' + project_id + '/latest/');
        }.bind(this);
    },
    renderResults: function() {
        if (this.state.results.length) {
            return <div className="results">{ this.state.results.map(function(result) {
                switch (result._type) {
                    case 'project':
                        return <div className="result result-project" onClick={this.loadProjectReport(result._id)}>
                            <div className="programme">{result._source.programme}</div>
                            <div className="title">{result._source.title}</div>
                        </div>;
                    case 'programme':
                        return <div className="result result-programme">
                            {result._source.title}
                        </div>;
                }
            }.bind(this))}</div>;
        }
    },
    render: function() {
        var insight = require('../images/insight.png');

        var searchClassName = this.state.results.length ? 'has-results' : 'no-results';

        return <header>
            <div className="logo">
                <img src={insight} alt="inSight" />
            </div>
            <nav className="menu">
                <ul>
                    <li><a href="#">Progress</a></li>
                    <li><a href="#">Performance</a></li>
                    <li><a href="#">Projects</a></li>
                    <li><a href="#" onClick={this.logout}>Logout</a></li>
                </ul>
            </nav>
            <div className="search">
                <input className={searchClassName} type="search" ref="query" placeholder="Search Here" onChange={this.search} />
                {this.renderResults()}
            </div>
        </header>;
    }
});
module.exports = Header;
