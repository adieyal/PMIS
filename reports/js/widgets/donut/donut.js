define(['jquery', 'd3', 'text!widgets/donut/base.svg'], function($, d3, svg) {
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
	    
	    var node = d3.select(me.svg[0]);
	    
	    var content = node.selectAll('g.dynamic').data([0]);
	    content.enter().append('svg:g').attr('class', 'dynamic');
	    content.exit().remove();
	    
	    /* Draw the donut segments. */
        var arc = d3.svg.arc().outerRadius(35).innerRadius(18);
	    
        var pie = d3.layout.pie().value(function(d, i) {
		if (typeof d === 'number') {
		    return d;
		} else {
		    if (d && (typeof d === 'number')) {
                return d;
		    } else {
                return 0;
		    }
		}});
	    
        var total = me.data.values.reduce(function(a, b) { return a + b });

        var is_grey = false;
        if (total == 0) {
            me.data.values = [0, 0, 0, 1];
            is_grey = true;
        }

        var as_percentage = me.data.as_percentage
	    var arcs = content.selectAll('g.pie.slice').data(pie(me.data.values));
	    arcs.enter().append('svg:g').attr('class', function(d, i) {
            if (is_grey) return 'pie slice slice-grey';
            return 'pie slice slice'+i;
	    });

	    arcs.exit().remove();
	    var paths = arcs.append('svg:path');
	    paths.attr('d', arc);
	    
	    /* And then place the labels. */
            var arc = d3.svg.arc().outerRadius(43).innerRadius(43);

	    arcs.append("svg:text") 
		.attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; }) 
		.attr("dy", "0.5em") 
		.attr("text-anchor", "middle") 
		.attr("display", function(d) { return d.value >= 0.02 ? null : "none"; }) 
		.text(function(d, i) {
            if (is_grey) return "";

            if (as_percentage)
                return (d.value * 100).toFixed(0) + "%"
            else
                return (d.value)
        });
	    return;
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
