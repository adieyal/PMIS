require.config({
    baseUrl: '../js'
});

require(['jquery'], function($) {
    /* Set variable when done rendering. */
    (function() {
	var widget_count = $('[data-widget]').length;
	var widget_rendered = 0;
	$(document).on('widget-rendered', function() {
	    widget_rendered++;
	    if (widget_rendered == widget_count) {
		widget_render_done = true;
	    }
	});
    })();
    
    $.fn.widget = function(options) {
	this.each(function() {
	    var element = $(this);
	    var widget = element.data('widget');
	    require([widget], function(Widget) {
		var w = new Widget(element[0]);
		if (!w.can_render()) {
		    element.pngWidget();
		} else {
		    element.data('widget-instance', w);
		    w.init(element);
		}
	    });
	});
	return this;
    }
    $.fn.pngWidget = function(options) {
	this.each(function() {
	    var element = $(this);
	    var id = element.attr('id');
	    if (typeof(id) == 'undefined') {
		alert('Unable to generate PNG widget for element with no \'id\'.');
	    } else {
		console.log('pngWidget');
		console.log('u='+window.location.href);
		console.log('s='+id);
	    }
	});
	return this;
    }
    $(document).ready(function() {
	$('[data-widget]').widget()
    });
});
