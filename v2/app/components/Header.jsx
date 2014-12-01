var React = require("react");
var StoreMixin = require('../mixins/StoreMixin');
var AuthStore = require("../stores/AuthStore");
var AuthActions = require("../actions/AuthActions");

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

        var query = this.refs.query.getDOMNode().value;

        var remote = require('../lib/remote');
        currentRequest = remote.search(query, AuthStore.getState().auth_token, function(results) {
            this.setState({
                loading: false,
                results: results
            });
        }.bind(this));
    },
    logout: function() {
        var remote = require('../lib/remote');
        remote.logout(function() {
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
        var auth = this.props.auth;

        var insight = require('../images/insight.png');

        var searchClassName = this.state.results.length ? 'has-results' : 'no-results';

        if (auth.status == 'logged-in') {
            return <header>
                <div className="logo">
                    <a href="#" onClick={this._owner.showDashboard}><img src={insight} alt="inSight" /></a>
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
        } else {
            return <header>
                <div className="logo">
                    <img src={insight} alt="inSight" />
                </div>
            </header>;
        }
    }
});
module.exports = Header;
