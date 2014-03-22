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
	    
	    var stage = me.data[0];
	    var progress = me.data[1] || 0;
	    
	    console.log(stage, progress);
	    
	    node.addClass('project-stage-'+stage);
	    node.find('.stage-progress').text(Math.round(progress)+'%');
	    node.find('.stage-progress').css('left', progress+'%');
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
