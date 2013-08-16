require.config({
    baseUrl: "/static/js/",
    paths: {
        jquery : "lib/jquery",
        text : "lib/text",
        d3 : "lib/d3",
    },
    shim: {
        "lib/jquery": {
            exports: '$'
        },
        "lib/d3": {
            exports: 'd3'
        },
        "lib/jquery.number": ['jquery'],
    },
});

require(['lib/jquery', 'widgets/js/widgets'], function($, widgets) {
    map = $("#map")[0]
    mapdoc = $(map.contentDocument)
    mapdoc.find("#m_lekwa").css("fill", "red")
    /*
    All we need to get going is widgets.js
    Once it is loaded, it scans through the page picking
    up data-widget attributes and drawing the appropriate widgets
    */
})
