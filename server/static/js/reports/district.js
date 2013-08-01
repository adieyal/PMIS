define(["lib/jquery", "lib/jquery.number", "widgets/js/widgets"], function($, ignore, widgets) {
    district = function(year, month) {
        this.year = year;
        this.month = month;
    }

    district.prototype = {
        dt_format : function(dt) {
            months = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
            ];

            month = months[dt.getMonth()];
            year = dt.getYear();
            return month + " " + (1900 + year);
                        
        },
        num_format : $.number,
        perc_format : function(n) { return this.num_format(n * 100) + "%"; },
        cur_format : function(n) { return "R " + this.num_format(n); },

        client_colors : {
            "DoE"  : "client-doe",
            "DCSR" : "client-dcsr",
            "DEDET": "client-dedet",
            "DoH"  : "client-doh",
            "DSD"  : "client-dsd",
            "DSSL" : "client-dssl"
        },

        client_colors2 : {
            "DoE" :"#9792b3",
            "DCSR" :"#e7bb5e",
            "DEDET" :"#e4cfbf",
            "DoH" :"#8cc6ec",
            "DSD" :"#b9b387",
            "DSSL" :"#bd7794"
        },

        fn_slider : function(client, position1, position2, text1, text2) {
            if (position1 < 0.1) position1 = 0.1
            if (position2 < 0.1) position2 = 0.1
            if (position1 > 0.9) position1 = 0.8
            if (position2 > 0.9) position2 = 0.8

            threshold = 0.2;
            text1 = text1 || "Actual"
            text2 = text2 || "Planned"

            barcolor2 = this.client_colors2[client];
            if (position2 - position1 > threshold) {
                barcolor2 = "#f04338";
            }

            barcolor1 = this.client_colors2[client];
            if (position1 - position2 > threshold) {
                barcolor1 = "#f04338";
            }
            if (Math.abs(position1 - position2) < 0.1) {
                //text2 = text1 + "/" + text2
                text1 = " ";
            }
            el1 = {
                    "position": position1,
                    "bar-color": barcolor1,
                    "marker-color": "#656263",
                    "marker-style": "short",
                    "marker-text": text1
            } 

            el2 = {
                    "position": position2,
                    "bar-color": barcolor2,
                    "marker-color": "#f04338",
                    "marker-style": "long",
                    "marker-text": text2
            }  

            if (position1 > position2)
                return [el2, el1]
            else
                return [el1, el2]
        },

        fn_gauge : function(position1, position2, text1, text2) {
            if (Math.abs(position1 - position2) < 0.05)
                text1 = " "

            return [{
                "position": position1,
                "text": text1 || "Planned",
                "needle-style": "dashed"
            },
            {
                "position": position2,
                "text": text2 || "Actual",
                "needle-color": ["#86bf53", "#cce310"],
                "needle-style": "plain"
            }]
        },

        populate_general : function(json) {
            $(".district-name").text(json["name"]);
            $(".district-text .date").text(this.dt_format(new Date(this.year, this.month - 1, 1)))
        },

        populate_client_names : function(json) {
            $("#department-projects").each(function() {
                
                me = jQuery(this);
                clients = json["clients"]
                me.find(".department-name div").each(function(id) {
                    $(this).text(clients[id]["fullname"]);
                });
            })
        },

        populate_total_projects : function(json) {
            $("#department-projects").each(function() {
                
                me = jQuery(this);
                clients = json["clients"]
                me.find(".total_projects span").each(function(id) {
                    $(this).text(clients[id]["total_projects"]);
                });

                me.find(".cfye .right").each(function(id) {
                    $(this).text(clients[id]["projects"]["completed_in_fye"])
                });

                me.find(".cipl .right").each(function(id) {
                    $(this).text(clients[id]["projects"]["currently_in_planning"])
                });

                me.find(".inimpl .right").each(function(id) {
                    $(this).text(clients[id]["projects"]["currently_in_implementation"])
                });

                me.find(".fincom .right").each(function(id) {
                    $(this).text(clients[id]["projects"]["currently_in_final_completion"])
                });

                me.find(".praccom .right").each(function(id) {
                    $(this).text(clients[id]["projects"]["currently_in_practical_completion"])
                });

                me.find(".project-pie").each(function(id) {

                    var w = $(this).data('widget-instance');
                    w.data = new Array();
                    prdata = clients[id]["projects"]

                    for (var key in prdata) {
                        w.data.push(prdata[key]);
                    }
                    w.draw();
                });
            })
        },

        populate_clients : function(json) {
            var dist = this;
            $("#department-projects").each(function() {
                
                /*
                me = jQuery(this);
                clients = json["clients"]
                me.find(".department-name div").each(function(id) {
                    $(this).text(clients[id]["fullname"]);
                });
                */

                me.find(".project-budget span").each(function(id) {
                    $(this).text(dist.cur_format(clients[id]["total_budget"]));
                });

                me.find(".num-of-job span").each(function(id) {
                    $(this).text(dist.num_format(clients[id]["num_jobs"]));
                });

                me.find(".overall span").each(function(id) {
                    val = clients[id]["overall_progress"]["actual"] / 100;
                    $(this).text(dist.perc_format(val));
                });

                me.find(".implementation-text span").each(function(id) {
                    val = clients[id]["overall_expenditure"]["perc_expenditure"]
                    $(this).text(dist.perc_format(val));
                });

                me.find(".actual-text span").each(function(id) {
                    val = clients[id]["overall_expenditure"]["actual_expenditure"]
                    $(this).text(dist.cur_format(val));
                });

                me.find(".client-slider").each(function(id) {
                    var a = clients[id]["overall_expenditure"]["actual_expenditure"]
                    var p = clients[id]["overall_expenditure"]["planned_expenditure"]
                    var b = clients[id]["total_budget"]

                    var w = $(this).data('widget-instance');
                    if (b == 0) {
                        w.data = dist.fn_slider(clients[id]["name"],0.0, 0.0);
                    } else {
                        w.data = dist.fn_slider(clients[id]["name"],a/b, p/b);
                    }
                    w.draw();
                });
            });
            $(".progress-gauge").each(function(id) {
                actual = json["clients"][id]["overall_progress"]["actual"] / 100
                planned = json["clients"][id]["overall_progress"]["planned"] / 100

                var w = $(this).data('widget-instance');
                w.data = dist.fn_gauge(actual, planned);
                w.draw();
            });
        },

        populate_project : function(json) {
            dist = this;
            populate_item = function(datum, project_node) {
                var client_name = datum["client"]
                project_node.find(".project-name").each(function(id) {
                    cls = dist.client_colors[client_name];
                    $(this).addClass("client-doe");
                });

                project_node.find(".project-location").each(function(id) {
                    var val = datum["municipality"]["name"];
                    $(this).text(val);
                });

                project_node.find(".pname").each(function(id) {
                    var val = datum["name"];
                    $(this).text(val);
                });

                project_node.find(".project-department").each(function(id) {
                    var val = datum["client"];
                    $(this).text(val);
                });

                project_node.find(".total-budget .price").each(function(id) {
                    var val = dist.cur_format(datum["budget"]);
                    $(this).text(val);
                });

                project_node.find(".overall-progress .progress").each(function(id) {
                    var val = dist.perc_format(datum["progress"]["actual"]);
                    $(this).text(val);
                });

                project_node.find(".num-jobs .jobs").each(function(id) {
                    var val = dist.num_format(datum["jobs"]);
                    $(this).text(val);
                });

                project_node.find(".implementation-expenditure .expenditure").each(function(id) {
                    var val = dist.perc_format(datum["expenditure"]["ratio"]);
                    $(this).text(val);
                });

                project_node.find(".actual-expenditure .expenditure").each(function(id) {
                    var val = dist.cur_format(datum["expenditure"]["actual"]);
                    $(this).text(val);
                });

                project_node.find(".progress-slider").each(function(id) {
                    var a = datum["progress"]["actual"];
                    var p = datum["progress"]["planned"];
                    w = $(this).data('widget-instance');
                    w.data = dist.fn_slider(datum["client"], a, p);
                    w.draw();
                });

                project_node.find(".expenditure-slider").each(function(id) {
                    var a = datum["expenditure"]["actual"];
                    var p = datum["expenditure"]["planned"];
                    w = $(this).data('widget-instance');
                    w.data = dist.fn_slider(datum["client"], a, p);
                    w.draw();
                });
            }

            $(".top-performing-projects .project").each(function(id) {
                var me = jQuery(this);
                var data = json["projects"]["best_performing"]
                populate_item(data[id], me);
            });

            $(".worst-performing-projects .project").each(function(id) {
                var me = jQuery(this);
                var data = json["projects"]["worst_performing"]
                populate_item(data[id], me);
            });
        },

        populate_department_projects : function(json) {
            $("#department-projects-counts .department").each(function(id) {
                var me = jQuery(this);
                var datum = json["clients"][id]
                me.find(".department-name").each(function() {
                    $(this).text(datum["fullname"])
                });

                me.find(".department-num").each(function() {
                    $(this).text(datum["total_projects"])
                });
            });
        },

        populate_dashboard : function(json) {
            this.populate_general(json);
            this.populate_client_names(json);
            this.populate_clients(json);
            this.populate_project(json);
            this.populate_department_projects(json);
        },

        populate_progress : function(json) {
            this.populate_general(json);
            this.populate_client_names(json);
            this.populate_total_projects(json);
        }
    }
    return district
});
