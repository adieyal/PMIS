var component = require('omniscient').withDefaults({ jsx: true });
component.debug();

var React = require('react');

var lists = require('../lib/lists');
var AuthStore = require('../stores/AuthStore');
var ClusterStore = require('../stores/ClusterStore')(lists.clusters);
var PreferenceStore = require('../stores/PreferenceStore');
var ProjectStore = require('../stores/ProjectStore');

var PreferenceActions = require('../actions/PreferenceActions');

var logo = require('../images/insight.png');

var App = require('./App');

function render() {
    var auth = AuthStore.cursor();
    var preference = PreferenceStore.cursor().deref();
    var view = auth.get('status') == 'logged-in' ?
        preference.get('view') : 'login';

    var clusters = ClusterStore.cursor('clusters');
    var projects = ProjectStore.cursor('projects');

    if (clusters.size < lists.clusters.length || projects.size == 0) {
        React.render(
            <div className="ui active inverted dimmer">
                <div className="ui text loader">Loaded {clusters.size} clusters</div>
            </div>, document.body);
    } else {
        React.render(
            <App
                auth={AuthStore.cursor()}
                view={view}
                clusters={clusters}
                logo={logo}
                preference={preference}
                projects={projects}
            />, document.body);
    }
}

AuthStore.on('swap', render);
ClusterStore.on('swap', render);
PreferenceStore.on('swap', render);
ProjectStore.on('swap', render);

render();

if (typeof window !== 'undefined') {
    var parts = window.location.hash.replace('#/', '').split('/');

    if (parts.length > 0) {
        PreferenceActions.setPreference('view', parts[0] || 'dashboard');
    }
}
