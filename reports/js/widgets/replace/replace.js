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
		
		if ((typeof(id) != 'undefined') && (typeof(me.data[id] != 'undefined'))) {
		    element.text(me.data[id]);
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
