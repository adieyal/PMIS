import React from 'react/addons';
import lists from '../lib/lists';
import Dashboard from './Dashboard';
import LoginForm from './LoginForm';
import Template from './Template';

import { setPreference } from '../actions';

import ClusterProgress from './ClusterProgress';
import ClusterPerformance from './ClusterPerformance';
import ClusterProjects from './ClusterProjects';

if (typeof window != 'undefined') {
    /** This can only be done in the browser */
    jQuery = require('jquery');

    require('jquery-address');

    require('semantic-ui');
    require('../styles/screen.css');

    /** How to get to the backend */
    jQuery.fn.api.settings.api = {
        search: BACKEND + '/reports/search?query={query}',
        cluster: BACKEND + '/reports/project/department-of-{slug}/latest/'
    };

    jQuery.QueryString = (function(a) {
        if (a == "") return {};
        var b = {};

        for (var i = 0; i < a.length; ++i) {
            var p=a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }

        return b;
    })(window.location.search.substr(1).split('&'));
}

var AddressState = {
    getInitialState: function() {
        return {
            clusterId: lists.clusters[0].slug
        };
    },
    componentDidMount: function() {
        if(typeof window != 'undefined') {
            jQuery.address.change(function (evt) {
                this.changeAddress(evt);
            }.bind(this));
        }
    },
    changeAddress: function(evt) {
        if (this.isMounted()) {
            var state = {
                clusterId: lists.clusters[0].slug
            };

            var parts = evt.path.split('/').slice(1);

            if (parts.length > 0) {
                PreferenceActions.setPreference('view', parts[0] || 'dashboard');
            }

            if (parts.length > 1) {
                state.clusterId = parts[1] || lists.clusters[0].slug;
            }

            console.log(evt);

            if (parts.length > 2) {
                state.programme = parts[2];
            }

            if (parts.length > 3) {
                state.phase = parts[3];
            }

            if (parts.length > 4) {
                state.status = parts[4];
            }

            this.setState(state);
        }
    }
};

const App = ({ view, auth, preference, clusters, districts, projects }) => {
    var content;

    switch(view) {
        case 'login':
            content = <LoginForm auth={auth} />;
            break;
        case 'dashboard':
            content = <Dashboard preference={preference} clusters={clusters} districts={districts} />;
            break;
        case 'progress':
            content = <ClusterProgress clusters={clusters} />;
            break;
        case 'performance':
            content = <ClusterPerformance clusters={clusters} />;
            break;
        case 'projects':
            content = <ClusterProjects
                clusterId={this.state.clusterId}
                programme={this.state.programme}
                phase={this.state.phase}
                status={this.state.status}
                projects={projects} />;
            break;
    }

    return <Template
        auth={auth}
        preference={preference}>
        {content}
    </Template>;
};

export default App;
