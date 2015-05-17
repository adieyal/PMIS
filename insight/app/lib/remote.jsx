var utils = require('../lib/utils');
var request = require('superagent');
var AuthActions = require('../actions/AuthActions');
var ClusterActions = require('../actions/ClusterActions');
var ProjectActions = require('../actions/ProjectActions');
var NotificationActions = require('../actions/NotificationActions');

function url(path) {
    return BACKEND + '/' + path;
}

Remote = {
    fetchProjects: function (authToken, query) {
        return request
            .get(url('reports/projects/' + query.year + '/' + query.month + '/'))
            .set('Accept', 'application/json')
            .set('Authorization', 'Token ' + authToken)
            .end(function (error, res) {
                if(error) {
                    return NotificationActions.notify(error);
                }

                if(res.body.error) {
                    return NotificationActions.notify(res.body.error);
                }

                ProjectActions.receiveProjects(res.body.data);
            });
    },
    fetchCluster: function (slug, authToken, query) {
        var month = parseInt(query.month);
        if(month < 10) month = '0' + month;
        return request
            .get(url('reports/cluster/department-of-' + slug + '/' + query.year + '/' + month + '/v2'))
            .set('Accept', 'application/json')
            .set('Authorization', 'Token ' + authToken)
            .end(function (error, res) {
                if(error) {
                    return NotificationActions.notify(error);
                }

                if(res.body.error) {
                    return NotificationActions.notify(res.body.error);
                }

                var cluster = res.body;
                ClusterActions.receiveCluster(slug, cluster);
            });
    },
    fetchClusters: function (clusters, authToken, query) {
        utils.each(clusters, function(cluster) {
            Remote.fetchCluster(cluster.slug, authToken, query);
        });
    },
    login: function (username, password) {
        return request
            .post(url('auth/login'))
            .send({ username: username, password: password })
            .set('Accept', 'application/json')
            .end(function (error, res) {
                if(error) {
                    return NotificationActions.notify(error);
                }

                if(res.status == 400) {
                    return AuthActions.loginFailure(res.body);
                }

                if(res.status != 200) {
                    return NotificationActions.notify(res.text);
                }

                AuthActions.login(res.body.auth_token);
            });
    },
    logout: function () {
        return request
            .post(url('auth/logout'))
            .set('Accept', 'application/json')
            .end(function (error, res) {
                if(error && error.status !== 401) return NotificationActions.notify(error);
                AuthActions.logout();
            });
    },
    search: function (query, authToken, done) {
        return request
            .get(url('reports/search') + '?query=' + query)
            .set('Accept', 'application/json')
            .end(function (error, res) {
                if(error) {
                    if(error.message && error.message == 'timeout of undefinedms exceeded') {
                        // We've been aborted
                        return;
                    }

                    return NotificationActions.notify(error);
                }

                done(res.body);
            });
    },
    searchProgrammes: function (clusterId, query, authToken, done) {
        return request
            .get(url('reports/search/programmes') + '?query=' + query + '&clusterId=' + clusterId)
            .set('Accept', 'application/json')
            .end(function (error, res) {
                if(error) {
                    if(error.message && error.message == 'timeout of undefinedms exceeded') {
                        // We've been aborted
                        return;
                    }

                    return NotificationActions.notify(error);
                }

                done(res.body);
            });
    },
};

module.exports = Remote;
