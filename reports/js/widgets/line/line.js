define(['d3', 'text!widgets/line/base.svg'], function(d3, svg) {
    /* Taken from force_labels.js. */
    (function() {
	d3.force_labels = function force_labels() {    
	    var labels = d3.layout.force();
	    var labels2 = d3.layout.force()
		.gravity(0).charge(-40).chargeDistance(30);
	    
	    // Update the position of the anchor based on the center of bounding box
	    function updateAnchor() {
		if (!labels.selection) return;
		labels.selection.each(function(d) {
		    var bbox = this.getBBox(),
		    x = bbox.x + bbox.width / 2,
		    y = bbox.y + bbox.height / 2;
		    
		    d.anchorPos.x = x;
		    d.anchorPos.y = y;
		    
		    // If a label position does not exist, set it to be the anchor position 
		    if (d.labelPos.x == null) {
			d.labelPos.x = x;
			d.labelPos.y = y;
		    }
		});
	    }
	    
	    //The anchor position should be updated on each tick
	    labels.on("tick.labels", updateAnchor);
	    
	    // This updates all nodes/links - retaining any previous labelPos on updated nodes
	    labels.update = function(selection) {
		labels.selection = selection;
		var nodes = [], links = [];
		var nodes2 = [], links2 = [];
		selection[0].forEach(function(d) {    
		    if(d && d.__data__) {
			var data = d.__data__;
			
			if (!d.labelPos) d.labelPos = {fixed: false};
			if (!d.anchorPos) d.anchorPos = {fixed: true};
			
			// Place position objects in __data__ to make them available through 
			// d.labelPos/d.anchorPos for different elements
			data.labelPos = d.labelPos;
			data.anchorPos = d.anchorPos;
			
			links.push({target: d.anchorPos, source: d.labelPos});
			nodes.push(d.anchorPos);
			nodes.push(d.labelPos);
			
			nodes2.push(d.labelPos);
			for (i=0; i<links2.length; i++) {
			    var elem = links2[i];
			    links2.push({target: d.labelPos, source: elem});
			};
		    }
		});
		labels
		    .stop()
		    .nodes(nodes)
		    .links(links);
		labels2
		    .stop()
		    .nodes(nodes2)
		    .links(links2);
		updateAnchor();
		labels.start();
		labels2.start();
	    };
	    return labels;
	};
    })();
    /* End of force_labels.js. */



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
		    .text(d.formatMoney(0))
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
		    .attr('x', 42)
		    .attr('y', 19+8*i);
		    /*.attr('x', x(labelx-2*i))
		    .attr('y', y(d.values[labelx-2*i][1]));*/
		/*
		var value_labels = line.selectAll('text.value').data(d.values);
		value_labels.enter().append('text').attr('class', 'value');
		value_labels.attr('x', function(d, i) { return x(d[0]); })
		    .attr('y', function(d, i) { return y(d[1]); })
		    .attr('dy', '-0.35em')
		    .text(function(d, i) { if (d[1]) { return d[1].formatMoney(0); }; return ''; });
		*/
	    });
	    
	    /* Build the value labels and their force layout. */
	    (function(dynamic) {
		var labels, links;
		
		function redraw() {
		    labels
			.attr("x",function(d) { return d.labelPos.x})
			.attr("y",function(d) { return d.labelPos.y});
			/*.attr("transform",function(d) { return "translate("+d.labelPos.x+" "+d.labelPos.y+")"})*/
		    
		    links
			.attr("x1",function(d) { return d.anchorPos.x})
			.attr("y1",function(d) { return d.anchorPos.y})
			.attr("x2",function(d) { return d.labelPos.x})
			.attr("y2",function(d) { return d.labelPos.y})
		}        
		
		
		// Initialize the label-forces
		labelForce = d3.force_labels()
		    .linkDistance(5)
		    .linkStrength(1)
		    .gravity(0)
		    .charge(0)
		    .on("tick",redraw);
		
		var container = dynamic.selectAll('g.labels').data([0])
		    .enter()
		    .append('g')
		    .attr('class', 'labels');
		dynamic.selectAll('g.line').each(function(d, i) {
		    var data = d.values;
		    var group = container.selectAll('g.labels-'+i).data([0])
			.enter().append('g').attr('class', 'labels-'+i);
		    var group_top = container.selectAll('g.top-labels-'+i).data([0])
			.enter().append('g').attr('class', 'top-labels-'+i);
		    var anchor = group.selectAll('circle.anchor').data(data);
		    anchor.enter().append('circle').attr('class', 'anchor');
		    anchor.attr('cx', function(d, i) { return x(d[0]); })
			.attr('cy', function(d, i) { return y(d[1]); })
			.attr('r', 1);

		    var label = group_top.selectAll('text.label').data(data);
		    label.enter().append('text').attr('class', function(d, i) {
			if (d[1]) { return 'label'; } else { return 'label label-zero' }
		    });
		    label.attr('x', function(d, i) { return x(d[0]); })
			.attr('y', function(d, i) { return y(d[1]); })
			.attr('dy', '0.35em')
			.text(function(d, i) { return d[1].formatMoney(0) });
		    
		    var link = group.selectAll('line.link').data(data);
		    link.enter().append('line').attr('class', function(d, i) {
			if (d[1]) { return 'link'; } else { return 'link link-zero' }
		    });
		    /*
		    label.attr('x1', function(d, i) { return x(d[0]); })
			.attr('x2', function(d, i) { return x(d[0]); })
			.attr('y1', function(d, i) { return y(d[1]); })
			.attr('y2', function(d, i) { return y(d[1]); });
		    */
		});
		links = container.selectAll('.link');
		labels = container.selectAll('text.label');
		container.selectAll('circle.anchor').call(labelForce.update);
	    })(d);
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
