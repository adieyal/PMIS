require(['jquery'], function($) {
    Number.prototype.formatMoney = function(c, d, t){
	var n = this, 
	c = isNaN(c = Math.abs(c)) ? 2 : c, 
	d = d == undefined ? "." : d, 
	t = t == undefined ? "," : t, 
	s = n < 0 ? "-" : "", 
	i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
	j = (j = i.length) > 3 ? j % 3 : 0;
	return 'R' + s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    };

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
	    require(['widgets/js/'+widget], function(Widget) {
		var w = new Widget(element[0]);
		if (!w.can_render()) {
		    element.pngWidget();
		} else {
		    element.data('widget-instance', w);
		    w.init(element);
		}
	    });
	});
	/* Call PhantomJS if this is run inside it to notify it that
	 * we are done rendering all widgets. */
	if (typeof window.callPhantom === 'function') {
	    window.callPhantom({ done: true });
	}
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
