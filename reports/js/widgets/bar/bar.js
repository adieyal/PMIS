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
	    var values = data.map(function(x) { return x.value || 0; });
	    var scale = d3.scale.linear()
		.domain([0, d3.max(values)]).nice(5)
		.range([90, 20]);
	    var ticks = scale.ticks(5);
	    
	    var labels = d.selectAll('g.label').data(ticks);
	    labels.enter().append('g');
	    labels.attr('class', function(d, i) { return 'label label-'+i; });
	    labels.each(function(d, i) {
		var label = d3.select(this);
		label.append('line')
		    .attr('x1', 40)
		    .attr('x2', 280)
		    .attr('y1', scale)
		    .attr('y2', scale);
		label.append('text')
		    .text(d)
		    .attr('x', 35)
		    .attr('y', scale)
		    .attr('dy', '0.35em');
	    });
	    
	    /* Build the bars and their labels. */
	    var x = d3.scale.linear()
		.domain([0, data.length]).range([40, 280]);
	    var bars = d.selectAll('g.bar').data(data);
	    bars.enter().append('g');
	    bars.attr('class', function(d, i) { return 'bar bar-'+i; });
	    bars.each(function(d, i) {
		var bar = d3.select(this);
		bar.append('rect')
		    .attr('x', x(i+0.25))
		    .attr('y', scale(d.value))
		    .attr('width', x(0.5)-x(0))
		    .attr('height', scale(0)-scale(d.value));
		bar.append('text')
		    .text(d.label)
		    .attr('dy', '1.1em')
		    .attr('x', x(i+0.5))
		    .attr('y', 90);
		bar.append('text')
		    .text(d.value.formatMoney(0))
		    .attr('dy', '-0.1em')
		    .attr('x', x(i+0.5))
		    .attr('y', scale(d.value));
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
