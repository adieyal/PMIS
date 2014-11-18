var React = require("react");

var NotificationStore = require('./NotificationStore');
var humane = require('humane-js');

require('../../node_modules/humane-js/themes/libnotify.css');

NotificationStore.addChangeListener(function() {
    var notification = NotificationStore.getLastNotification();
    var notify = humane.create();
    notify.log(notification);
});
