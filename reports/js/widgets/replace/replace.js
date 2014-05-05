define(['jquery'], function($) {
    Widget = function(element) {
	this.node = element;
    }
    Widget.prototype = {
	can_render: function() {
	    return true;
	},
	init: function() {
	    var node = $(this.node);

	    this.src = node.data('src');
	    this.draw();
	},
	draw: function() {
	    var me = this;
	    var node = $(me.node);
	    
	    if (!me.data) { me.load(); }
	    if (!me.data) { return; }

	    node.find('.replace').each(function() {
		var element = $(this);
		var id = element.attr('id');
		var attr = element.data('replace-attr');

		if ((typeof(id) != 'undefined') && (typeof(me.data[id] != 'undefined'))) {
		    if (attr) {
			element.attr(attr, me.data[id]);
		    } else {
			element.text(me.data[id]);
		    }
		}
	    });
	    
	    node.find('template.repeat').each(function() {
		var template = $(this);
		var html = template.html();
		var key = template.attr('id');
		var all_data = me.data[key];
		
		for (var i=0; i<all_data.length; i++) {
		    var data = all_data[i];
		    var el = $(html);

		    el.find('.replace').each(function() {
			var element = $(this);
			var id = element.attr('id');
			var attr = element.data('replace-attr');

			if ((typeof(id) != 'undefined') && (typeof(me.data[id] != 'undefined'))) {
			    if (attr) {
				element.attr(attr, data[id]);
			    } else {
				element.text(data[id]);
			    }
			}
		    });
		    
		    var widgets =  el.find('.widget')
		    for (j=0; j<widgets.length; j++) {
			var widget = $(widgets[j]);
			var src = widget.data('src');
			widget.data('src', src.replace('.i.', '.'+i+'.'));
			widget.widget({ data: data[src] });
		    };
		    
		    template.parent().append(el);
		}
	    });
	},
	load: function() {
	    var me = this;
	    var node = $(me.node);
	    var src = node.data('src');

	    if (src) {
		var url = src.split('#')[0];
		var sel = src.split('#')[1];
		$.ajax({
		    type: 'get',
		    url: url,
		    dataType: 'json',
		    async: false,
		    success: function(d) {
			if (sel) {
			    me.data = d[sel];
			} else {
			    me.data = d;
			}
		    },
		    error: function() { alert('Error loading data.'); }
		});
	    }
	}
    }
    return Widget;
});
