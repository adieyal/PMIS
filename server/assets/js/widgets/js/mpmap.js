define(['jquery', 'text!../mpmap/mpumalanga.svg'], function($, svg) {
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
            if (!me.data) { me.load(); }
            if (!me.data) { return; }

            me.set_municipality_colours()
            me.set_legend()
        },
        set_municipality_colours: function() {
            var me = this;
            var svg = $(me.node).find('svg');
            svg.find(".m_municipality").attr("class", "mpmap-allgood");
            for (el in me.data) {
                val = me.data[el];
                klass = "#m_" + el.replace(" ", "").toLowerCase();
                node = svg.find(klass);
                if (val >= 5) {
                    node.attr("class", "mpmap-lotsbad");
                } else if (val >= 3) {
                    node.attr("class", "mpmap-morebad");
                } else if (val > 0) {
                    node.attr("class", "mpmap-fewbad");
                }
            }
        },
        set_legend : function() {
            var me = this;
            var svg = $(me.node).find('svg');
            var legend = svg.find("#mp-legend")

            legend1 = svg.find("#mp-legend1") 
            legend1.find("rect").attr("class", "mpmap-allgood");
            legend1.find("rect").css({"fill": ""});
            y = parseInt(legend1.attr("y"))
            console.log(y)
             
            y += 150;
            legend2 = legend1.clone()
            legend2.attr("id", "mp-legend2");
            legend2.attr("transform", "translate(0," + y.toString() + ")");
            legend2.find("rect").attr("class", "mpmap-fewbad");
            legend2.find("rect").css({"fill": ""});
            legend2.find(".text").text("1 - 2")
            legend.append(legend2)

            y += 150;
            legend3 = legend1.clone()
            legend3.attr("id", "mp-legend3");
            legend3.attr("y", y.toString());
            legend3.attr("transform", "translate(0," + y.toString() + ")");
            legend3.find("rect").attr("class", "mpmap-morebad");
            legend3.find("rect").css({"fill": ""});
            legend3.find(".text").text("3 - 4")
            legend.append(legend3)

            y += 150;
            legend4 = legend1.clone()
            legend4.attr("id", "mp-legend4");
            legend4.attr("y", y.toString());
            legend4.attr("transform", "translate(0," + y.toString() + ")");
            legend4.find("rect").attr("class", "mpmap-lotsbad");
            legend4.find("rect").css({"fill": ""});
            legend4.find(".text").text("5+")
            legend.append(legend4)

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
