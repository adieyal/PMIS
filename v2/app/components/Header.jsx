var React = require("react");
var StoreMixin = require('../mixins/StoreMixin');
var AuthStore = require("../stores/AuthStore");
var AuthActions = require("../actions/AuthActions");
var ClusterProgress = require("./ClusterProgress");
var utils = require('../lib/utils');

var currentRequest;

var Header = React.createClass({
    mixins: [ 'events' ],
    events: {
        'ref:progress:click': 'showProgress'
    },
    showProgress: function() {
        this._owner.setState({ view: 'progress' });
    },
    getInitialState: function() {
        return {
            loading: false,
            results: []
        };
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
    componentDidMount: function() {
        jQuery('.ui .search').search({
            type: 'category'
        });
    },
    render: function() {
        var auth = this.props.auth;

        var insight = require('../images/insight.png');

        var searchClassName = this.state.results.length ? 'has-results' : 'no-results';

        if (auth.status == 'logged-in') {
            return <div className="ui menu">
                <a ref="home" className="active item"><i className="home icon" /> Home</a>
                <a ref="progress" className="item">Progress</a>
                <a ref="performance" className="item">Performance</a>
                <a ref="projects" className="item">Projects</a>
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
            </div>;
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
