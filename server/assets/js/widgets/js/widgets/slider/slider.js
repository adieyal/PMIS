define(['jquery', 'text!widgets/slider/base.svg'], function($, svg) {
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
	    node.html(svg);

	    this.src = node.data('src');
	    this.svg = node.find('svg');
	    this.aspect = (parseFloat(node.data('aspect')) || 1) * 90;
	    this.svg[0].setAttribute('viewBox', '-7 0 '+(this.aspect+18)+' 30');
	    this.svg.find('.outer-bar').attr('width', this.aspect);
	    this.svg.find('.inner-bar').attr('width', this.aspect-4);	    

	    this.draw();
	},
	draw: function() {
	    var me = this;
	    var svg = $(me.node).find('svg');
	    var d = svg.find('.dynamic');
	    var px = 0;
	    var bars = [];
	    var markers = [];
	    
	    if (!me.data) { me.load(); }
	    if (!me.data) { return; }
	    d.children().remove()
	    for (i=0; i<me.data.length; i++) {
		var data = me.data[i];
		var m = svg.find('#tpl-marker-'+(data['marker-style'] || 'short')).clone();
		var b = svg.find('#tpl-inner-bar').clone();
		var x = (me.aspect-4)*(data['position'] || 0);
		
		m.attr('id', 'marker'+i);
		m.attr('transform', 'translate('+x+',0)');
		if (data['marker-color']) {
		    var mgid = 'marker'+i+'-gradient';
		    m.find('.marker-accent').css('stroke', data['marker-color']);
		    me.addGradient(mgid, data['marker-color'], '#tpl-marker-inner-gradient');
		    m.find('.marker-inner').css('fill', 'url(#'+mgid+')');
		    m.find('.marker-inner').css('stroke', data['marker-color']);
		}
		if (data['marker-text']) {
		    m.find('.marker-text').text(data['marker-text']);
		} else {
		    m.find('.marker-text').remove();
		}
		
		b.attr('id', 'bar'+i);
		b.attr('x', px+4);
		b.attr('width', x-px);
		if (data['bar-color']) {
		    var gid = 'bar'+i+'-gradient';
		    me.addGradient(gid, data['bar-color']);
		    b.css('stroke', data['bar-color']);
		    b.css('fill', 'url(#'+gid+')');
		}
		
		px = x;
		
		bars.push(b);
		markers.push(m);		
	    }
	    d.append(bars);
	    d.append(markers);
	},
	addGradient: function(id, color, template) {
	    var me = this;
	    var svg = $(me.node).find('svg');
	    var defs = svg.find('defs');
	    var template = template || '#tpl-inner-gradient';
	    var gradient = defs.find(template).clone()
	    
	    gradient.attr('id', id);
	    gradient.find('stop').attr('stop-color', color);
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
