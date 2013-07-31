define(['jquery', 'text!../gauge/base.svg'], function($, svg) {
    Widget = function(element) {
	this.node = element;
    }
    Widget.prototype = {
	can_render: function() {
	    var svg = !!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', "svg").createSVGRect;
	    return svg;
	},
	init: function() {
	    var node = $(this.node);
	    var src = node.data('src');
	    this.src = node.data('src');
	    this.svg = node.find('svg');
	    
	    node.html(svg);
	    this.draw();
	},
	draw: function() {
	    var me = this;
	    var svg = $(me.node).find('svg');
	    var d = svg.find('.dynamic');
	    var px = 0;
	    var needles = [];
	    var markers = [];
	    
	    if (!me.data) { me.load(); }
	    if (!me.data) { return; }
	    d.children().remove()
	    for (i=0; i<me.data.length; i++) {
		var data = me.data[i];
		var n = svg.find('#tpl-gauge-needle-'+(data['needle-style'] || 'plain')).clone();
		var m = svg.find('#tpl-gauge-marker-'+(data['marker-style'] || 'plain')).clone();
		var a = Math.PI-Math.PI*(data['position'] || 0);
		var s = Math.abs(0.5-data['position'])*0.28+1;
		var x = Math.cos(a)*57*s;
		var y = 57-Math.sin(a)*57*s;
		
		m.attr('id', 'gauge-marker'+i);
		m.attr('transform', 'translate('+x+','+y+')');
		/*
		if (data['marker-color']) {
		    m.find('.marker-accent').css('stroke', data['marker-color']);
		}
		*/
		if (data['text']) {
		    m.find('.gauge-marker-text').text(data['text']);
		} else {
		    m.find('.gauge-marker-text').remove();
		}

		var r = 180*(data['position'] || 0)-90;
		n.attr('id', 'gauge-needle'+i);
		n.find('line').attr('y1', -57*s);
		n.find('rect').attr('y', -57*s);
		n.find('rect').attr('height', 57*s);
		n.attr('transform', 'rotate('+r+')');
		if (data['needle-color']) {
		    var gid = 'gauge-needle'+i+'-gradient';
		    me.addGradient(gid, data['needle-color']);
		    n.find('rect').css('fill', 'url(#'+gid+')');
		    m.find('.gauge-marker-inner').css('fill', 'url(#'+gid+')');
		}
		
		
		if (i==0) {
		    var green = Math.round(data['position']*25);
		    svg.find('.gauge-markers line').css('stroke', '#86bf53');
		    svg.find('.gauge-markers line:lt('+green+')').css('stroke', '#f0423e');
		}
		
		needles.push(n);
		markers.push(m);		
	    }
	    d.append(needles);
	    d.append(markers);
	    $(me.node).attr('data-rendered', true);
	    $(document).trigger('widget-rendered');
	},
	addGradient: function(id, color) {
	    var me = this;
	    var svg = $(me.node).find('svg');
	    var defs = svg.find('defs');
	    var gradient = defs.find('#tpl-gauge-needle-gradient').clone()
	    
	    gradient.attr('id', id);
	    $(gradient.find('stop')[0]).attr('stop-color', color[1]);
	    $(gradient.find('stop')[1]).attr('stop-color', color[0]);
	    $(gradient.find('stop')[2]).attr('stop-color', color[0]);
	    defs.append(gradient);
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
