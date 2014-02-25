define(['d3', 'text!widgets/line/base.svg'], function(ignore, svg) {
    Number.prototype.formatMoney = function(c, d, t){
	var n = this, 
	c = isNaN(c = Math.abs(c)) ? 2 : c, 
	d = d == undefined ? "." : d, 
	t = t == undefined ? "," : t, 
	s = n < 0 ? "-" : "", 
	i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
	j = (j = i.length) > 3 ? j % 3 : 0;
	return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    };
    
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
		    .text('R'+d.formatMoney(0))
		    .attr('x', 35)
		    .attr('y', y)
		    .attr('dy', '0.35em');
	    });
	    
	    d.append('g')
		.attr('transform', 'translate(9, 55) rotate(270)')
		.attr('class', 'ymainlabel')
		.append('text')
		.text('(in thousands)');
	    
	    /* Build the x-axis labels. */
	    var xlabels = d.selectAll('g.xlabel').data(me.data.labels);
	    xlabels.enter().append('g').attr('class', 'xlabel');
	    xlabels.each(function(d, i) {
		var label = d3.select(this);
		label.append('text')
		    .attr('x', x(i))
		    .attr('y', 90)
		    .attr('dy', '1.05em')
		    .text(d);
	    });

	    /* Build the lines and their labels. */
	    var lines = d.selectAll('g.line').data(data);
	    lines.enter().append('g');
	    lines.attr('class', function(d, i) { return 'line line-'+i; });
	    lines.each(function(d, i) {
		var l = d3.svg.line()
		    .x(function(d) { return x(d[0]); })
		    .y(function(d) { return y(d[1]); });
		var line = d3.select(this);
		line.append('path')
		    .attr('d', function(d, i) { return l(d.values); });
		line.append('text')
		    .text(d.label)
		    .attr('x', 42+40*i)
		    .attr('y', 19);
		    /*.attr('x', x(labelx-2*i))
		    .attr('y', y(d.values[labelx-2*i][1]));*/
		
		console.log(d.values);
		var value_labels = line.selectAll('text.value').data(d.values);
		value_labels.enter().append('text').attr('class', 'value');
		value_labels.attr('x', function(d, i) { return x(d[0]); })
		    .attr('y', function(d, i) { return y(d[1]); })
		    .attr('dy', '-0.35em')
		    .text(function(d, i) { if (d[1]) { return 'R'+d[1].formatMoney(0); }; return ''; });
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
