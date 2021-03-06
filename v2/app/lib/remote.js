var request = require('superagent');
var AuthActions = require('../actions/AuthActions');
var NotificationActions = require('../actions/NotificationActions');

function url(path) {
    return BACKEND + '/' + path;
}

module.exports = {
    fetchProjects: function (authToken, done) {
        return request
            .get(url('reports/projects'))
            .set('Accept', 'application/json')
            .set('Authorization', 'Token ' + authToken)
            .end(function (error, res) {
                if(error) {
                    return NotificationActions.notify(error);
                }

                if(res.body.error) {
                    return NotificationActions.notify(res.body.error);
                }

                var payload = res.body;
                done(payload);
            });
    },
    fetchCluster: function (slug, authToken, done) {
        return request
            .get(url('reports/cluster/department-of-' + slug + '/latest/dashboard/v2'))
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
                done(cluster);
            });
    },
    login: function (username, password, done) {
        return request
            .post(url('auth/login'))
            .send({ username: username, password: password })
            .set('Accept', 'application/json')
            .end(function (error, res) {
                if(error) return NotificationActions.notify(error);

                if(res.status == 400) {
                    return AuthActions.loginFailure(res.body);
                }

                if(res.status != 200) {
                    return NotificationActions.notify(res.text);
                }

                var data = res.body;
                data.username = username;
                done(data);
            });
    },
    logout: function (done) {
        return request
            .post(url('auth/logout'))
            .set('Accept', 'application/json')
            .end(function (error, res) {
                if(error && error.status !== 401) return NotificationActions.notify(error);
                done();
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
