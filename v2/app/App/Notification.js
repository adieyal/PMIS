var React = require("react");

var NotificationStore = require('./NotificationStore');

require('../../node_modules/humane-js/themes/libnotify.css');

NotificationStore.addChangeListener(function() {
    var notification = NotificationStore.getLastNotification();

    var humane = require('humane-js');
    var notify = humane.create();

    notify.log(notification);
});
