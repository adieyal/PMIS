/* Segment pie widget */
/*

Parameters
==========

width - width of embedded svg element (required)
height - height of embedded svg element (required)
radius - radius of the pie
arc.width - width of the circle arcs - larger values will reduce the doughnut effect. (default - 100)
arc.offset_x, arc.offset_y - shift the graph to the right and down (default - 0)
arc.margin - space between the arcs - only useful if the stroke colour is set to the background-colour in the css class. This displays segments separated rather than close together


Sample configuration snippet
"data" : [45, 23, 18, 5],
"width" : 400,
"height" : 400


TODO - this needs to be cleaned up
*/

define(['d3'], function(ignore) {
    Widget = function(element) {
        this.node = d3.select(element);
    }

    Widget.prototype = {
        can_render: function() {
            var svg = !!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', "svg").createSVGRect;
            return svg;
        },

        init : function() {
            this.ctx = {
                width: 153,
                height: 130,
                radius: 51,
                arc : {
                    width: 25,
                    offset_x : 25,
                    offset_y : 10,
                }
            }
            this.draw()
        },

        configure: function() {

            ctx = this.ctx
            if (!ctx) { return; }
            if (ctx === undefined || ctx.length === 0) { return; }

            if (ctx.width === undefined){ throw Error('No width given.'); }
            this.w = ctx.width;

            if (ctx.height === undefined){ throw Error('No height given.'); }
            this.h = ctx.height;

            // Radius of the circle
            this.r = ctx.radius || Math.min(this.w, this.h) / 2.1;

            // Arc config
            this.arc = ctx.arc || {};
            this.arc.width = this.arc.width || 100;
            this.arc.offset_x = this.arc.offset_x || 0; // x offset of the graph
            this.arc.offset_y = this.arc.offset_y || 0; // y offset of the graph
            this.arc.margin = this.arc.margin || 0.1; // margin between the arcs

            this.class = ctx.class || "chart"; // css class
            this.id = ctx.id || ""; // id


            this.colors = ctx.colors || ['#e7ce8b', '#d0cfae', '#bcb3d0', '#b6ded2'];
            this.empty_color = ctx.empty_color || "#d1d2d4";
        },

        draw_empty : function() {
            var me = this;

            var data = [10, 10];
            
            var total = 20;

            me.current_angle = 0;
            var arc = d3.svg.arc()
                .startAngle(function(d, i) { return me.current_angle; })
                .endAngle(function(d, i) {
                    me.current_angle = d / total * Math.PI * 2 + me.current_angle ;
                    return me.current_angle;
                })
                .innerRadius(this.r - this.arc.width)
                .outerRadius(this.r);

            this.vis = this.node.append("svg")
                .attr("class", this.class)
                .attr("width", this.w)
                .attr("height", this.h)
                .append('g')
                .attr("transform", "translate(" + (this.r + me.arc.offset_x) + "," + (this.r + me.arc.offset_y) + ")");

            // Add the arcs
            var paths = this.vis.selectAll('path')
                .data(data);

            paths.enter().append('path')
                .attr('d', arc)
                .attr('class', function(d, i) { return 'spg-arc spg-color spg-group-' + i +' spg-arc-' + i; })
                //.style('stroke', "#fff")
                .style('stroke-width', this.arc.margin / 2)
                .style('fill', function(d, i) { return me.empty_color; });
        },

        draw: function() {
            var me = this;
            if (!this.data) { return; }
            if (this.data.length === undefined || this.data.length === 0) { return; }
            this.configure()
            console.log(this.data);

            var total = 0;
            for (var i = 0 ; i < this.data.length; i++) {
                total += this.data[i];
            }

            if (total == 0) {
                this.draw_empty();
                return;
            }

            me.current_angle = 0;
            var arc = d3.svg.arc()
                .startAngle(function(d, i) { return me.current_angle; })
                .endAngle(function(d, i) {
                    me.current_angle = d / total * Math.PI * 2 + me.current_angle ;
                    return me.current_angle;
                })
                .innerRadius(this.r - this.arc.width)
                .outerRadius(this.r);

            var arc2 = d3.svg.arc()
                .startAngle(function(d, i) { return me.current_angle; })
                .endAngle(function(d, i) {
                    me.current_angle = d / total * Math.PI * 2 + me.current_angle ;
                    return me.current_angle;
                })
                .innerRadius(this.r)
                .outerRadius(this.r + this.arc.width * 1.2);


            this.vis = this.node.append("svg")
                .attr("class", this.class)
                .attr("width", this.w)
                .attr("height", this.h)
                .append('g')
                .attr("transform", "translate(" + (this.r + me.arc.offset_x) + "," + (this.r + me.arc.offset_y) + ")");

            // Add the arcs
            var paths = this.vis.selectAll('path')
                .data(this.data);

            paths.enter().append('path')
                .attr('d', arc)
                .attr('class', function(d, i) { return 'spg-arc spg-color spg-group-' + i +' spg-arc-' + i; })
                //.style('stroke', "#fff")
                .style('stroke-width', this.arc.margin / 2)
                .style('fill', function(d, i) { return me.colors[i]; });

            paths.enter().append('text')
                .attr("transform", function(d, i) { return "translate(" + arc2.centroid(d, i) + ")"; })
                .attr('text-anchor', 'middle')
                .attr('dy', '0.25em')
                .attr('class' , function(d, i){ return 'spg-arc-text spg-group-' + i; })
                .style('fill', '#fff')
                .text(function(d , i){ return d + '%'; });

        }
    };
    
    return Widget;
});

