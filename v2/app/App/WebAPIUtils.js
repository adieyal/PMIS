var request = require('superagent');
var NotificationActions = require('./NotificationActions');

function url(path) {
    return 'http://www.server.dev/' + path;
}

module.exports = {
    fetchCluster: function (slug, auth_token, done) {
        return request
            .get(url('reports/cluster/department-of-' + slug + '/latest/dashboard/new'))
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

                var data = res.body;
                data.username = username;
                done(data);
            });
    },
    logout: function (done) {
        return request
            .post(url('auth/logout'))
            .end(function (error, res) {
                if(error) return NotificationActions.notify(error);
                done();
            });
    }
};
