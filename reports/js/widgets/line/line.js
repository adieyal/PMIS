define(['d3', 'text!widgets/bar/base.svg'], function(ignore, svg) {
    Widget = function(element) {
	this.node = element;
    }
    Widget.prototype = {
	can_render: function() {
	    var svg_supported = !!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', "svg").createSVGRect;
	    return svg_supported;
	},
	init: function() {
	    var node = d3.select(this.node);
	    node.html(svg);

	    this.src = node.data('src');
	    this.svg = node.select('svg');   

	    this.draw();
	},
	draw: function() {
	    var me = this;
	    var svg = me.svg;
	    var d = svg.select('.dynamic');
	    
	    if (!me.data) { me.load(); }
	    if (!me.data) { return; }
	    
	    /* Clear all dynamic items for redraw. */
	    d.selectAll().remove()
	    
	    /* Main setup and add label. */
	    var data = me.data.data;
	    svg.select('text.title').text(me.data.title);
	    
	    /* Build the y-axis labels and grid. */
	    var xvalues = data.map(function(x) { return x.values.map(function(y) { return y[0]; }); });
	    var yvalues = data.map(function(x) { return x.values.map(function(y) { return y[1]; }); });
	    var labelx = 5;
	    
	    var ydiffmax = -1;
	    for (i=3; i<yvalues[0].length; i++) {
		var y1 = yvalues[0][i] || 0;
		var y2 = yvalues[1][i] || 0;
		var ydiff = Math.abs(y1-y2);
		if (ydiff > ydiffmax) {
		    labelx = i;
		    ydiffmax = ydiff;
		}
	    }
	    console.log(labelx);
	    var xmax = d3.max(data.map(function(x) { return d3.max(x.values.map(function(y) { return y[0]; })); }));
	    var ymax = d3.max(data.map(function(x) { return d3.max(x.values.map(function(y) { return y[1]; })); }));
	    var y = d3.scale.linear()
		.domain([0, d3.max([ymax, 100])]).nice(5)
		.range([90, 20]);
	    var x = d3.scale.linear()
		.domain([0, xmax]).range([40, 280]);
	    
	    var ticks = y.ticks(5);
	    
	    var labelnodes = [];
	    var labels = d.selectAll('g.label').data(ticks);
	    labels.enter().append('g');
	    labels.attr('class', function(d, i) { return 'label label-'+i; });
	    labels.each(function(d, i) {
		var label = d3.select(this);
		label.append('line')
		    .attr('x1', 40)
		    .attr('x2', 280)
		    .attr('y1', y)
		    .attr('y2', y);
		label.append('text')
		    .text(d)
		    .attr('x', 35)
		    .attr('y', y)
		    .attr('dy', '0.35em');
	    });
	    
	    /* Build the lines and their labels. */
	    var lines = d.selectAll('g.line').data(data);
	    lines.enter().append('g');
	    lines.attr('class', function(d, i) { return 'line line-'+i; });
	    lines.each(function(d, i) {
		console.log(d);
		var l = d3.svg.line()
		    .x(function(d) { return x(d[0]); })
		    .y(function(d) { return y(d[1]); });
		var line = d3.select(this);
		line.append('path')
		    .attr('d', function(d, i) { return l(d.values); });
		console.log(d.values[Math.floor(xmax/2)][1]);
		line.append('text')
		    .text(d.label)
		    .attr('dy', '-0.35em')
		    .attr('x', x(labelx-2*i))
		    .attr('y', y(d.values[labelx-2*i][1]));
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
