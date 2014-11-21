var React = require("react");
var WebAPIUtils = require('./WebAPIUtils');
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

        /*
        if (currentRequest) {
            currentRequest.abort();
        }
        */

        var query = this.refs.query.getDOMNode().value;
        currentRequest = WebAPIUtils.search(query, AuthStore.getState().auth_token, function(results) {
            this.setState({
                loading: false,
                results: results
            });
        }.bind(this));
    },
    handleSelect: function(selection) {
        console.log("SELECTION");
        console.log(selection);
    },
    logout: function() {
        WebAPIUtils.logout(function() {
            AuthActions.logout();
        });
    },
    renderResults: function() {
        if (this.state.results.length) {
            return <div className="results">{ this.state.results.map(function(result) {
                switch (result._type) {
                    case 'project':
                        return <div className="result result-project">
                            <div className="programme">{result._source.programme}</div>
                            <div className="title">{result._source.title}</div>
                        </div>;
                    case 'programme':
                        return <div className="result result-programme">
                            {result._source.title}
                        </div>;
                }
            })}</div>;
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
                <input className={searchClassName} type="search" ref="query" onChange={this.search} />
                {this.renderResults()}
            </div>
        </header>;
    }
});
module.exports = Header;
