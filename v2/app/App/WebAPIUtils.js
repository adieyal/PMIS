var request = require('superagent');
var AuthActions = require('./AuthActions');
var NotificationActions = require('./NotificationActions');

function url(path) {
    return BACKEND + '/' + path;
}

module.exports = {
    fetchCluster: function (slug, auth_token, done) {
        return request
            .get(url('reports/cluster/department-of-' + slug + '/latest/dashboard/v2'))
            .set('Authorization', 'Token ' + auth_token)
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
            .end(function (error, res) {
                console.log(res);
                if(error) return NotificationActions.notify(error);
                done();
            });
    },
    search: function (query, auth_token, done) {
        return request
            .get(url('reports/search') + '?query=' + query)
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
    searchProgrammes: function (cluster_id, query, auth_token, done) {
        return request
            .get(url('reports/search/programmes') + '?query=' + query + '&cluster_id=' + cluster_id)
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
