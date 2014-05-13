pmis = (function(jq) {
    var api = {
	base: '/'
    }
    var ui = {
	base: '/ui'
    }
    var session;

    /***** START OF AUTHENTICATION *****/
    
    /* This application requires that the user is authenticated
     * against the API. Check for authentication. */
    if (window.location.pathname != ui.base+'/login.html') {
	jq.ajax({
	    method: 'GET',
	    url: api.base+'account/session'
	}).success(function(data) {
	    var authenticated = data['authenticated'];
	    if (authenticated) {
		localStorage.setItem('next', null);
		session = data;
	    } else {
		/* User is not authenticated. Redirect to login page. */
		localStorage.setItem('next', window.location.href);
		window.location.href = ui.base+'/login.html';		
	    }
	}).error(function(status) {
	    alert('Something went wrong!');
	});
    } else {
	/* Bind all actions for the login page. */
	jq(document).ready(function() {
	    var form = jq('#login-form');
	    form.on('submit', function(e) {
		e.preventDefault();
		e.stopPropagation();
		
		var data = {};
		form.find('input[name]').each(function() {
		    var input = jq(this);
		    data[input.attr('name')] = input.val();
		});
		jq.ajax({
		    method: 'POST',
		    url: api.base+'account/login',
		    data: data
		}).success(function(data) {
		    if (data.success) {
			var next = localStorage.getItem('next');
			if (next == null) { next = ui.base+'/index.html'; }
			window.location.href = next;
		    } else {
			$('.login-panel input').removeClass('has-error');
			var errors = data['errors'];
			for (i=0; i<errors.length; i++) {
			    var field = errors[i]['field'];
			    var input = $('.login-panel input[name="'+field+'"]');
			    input.addClass('has-error');
			}
		    }
		}).error(function(status) {
		    alert('Something went wrong!');
		});
	    });
	});
    }
    
    function logout() {
	/* Redirect back to this page if logging back in. */
	localStorage.setItem('next', window.location.href);
	/* Log the user out. */
	jq.ajax({
	    method: 'GET',
	    url: api.base+'account/logout',
	}).success(function(data) {
	    if (data.success) {
		/* Redirect to login page. */
		var next = ui.base+'/login.html';
		window.location.href = next;
	    } else {
		alert('Something went wrong!');
	    }
	}).error(function(status) {
	    alert('Something went wrong!');
	});
	return false;
    }

    /***** END OF AUTHENTICATION *****/
    
    /***** START OF TEMPLATING *****/
    
    (function() {
	filters = {
	    all: function(data) {
		return true;
	    },
	    projects: function(data) {
		var cluster = localStorage.getItem('cluster-name');
		if (cluster) {
		    if (cluster == data.cluster) {
			return true;
		    } else {
			return false;
		    }
		} else {
		    return true;
		}
	    }
	}
	
	/* Take every template tag and render it. */
	jq('template').each(function() {
	    var template = $(this);
	    var render = Handlebars.compile(template.html());
	    var src = template.data('src');
	    var filter = template.data('filter');
	    var group = template.data('group-by');
	    
	    if (filter) {
		filter_func = filters[filter];
	    } else {
		filter_func = filters.all;
	    }
	    
	    jq.ajax({
		method: 'GET',
		url: src
	    }).success(function(data) {
		var items = data.filter(filter_func);
		if (group) {
		    var grouped = {};
		    var newItems = [];
		    for (i=0; i<items.length; i++) {
			var key = items[i][group];
			grouped[key] = [];
		    }
		    for (i=0; i<items.length; i++) {
			var key = items[i][group];
			grouped[key].push(items[i]);
		    }
		    for (key in grouped) {
			var gr = {
			    items: grouped[key]
			};
			gr[group] = key;
			newItems.push(gr);
		    }
		    items = newItems;
		}
		console.log(items);
		for (i=0; i<items.length; i++) {
		    var context = items[i];
		    console.log(context);
		    context['number'] = i+1;
		    var html = render(context);
		    template.after(html);
		}
		tempcharts();
	    });
	});
    })();

    /***** END OF TEMPLATING *****/
    
    /***** START OF PLOTS *****/
    /* This is just a placeholder for now. */
    function tempcharts() {
	var data1 = [
            [1, 43],
            [2, 35],
            [3, 49],
            [4, 31],
            [5, 45],
            [6, 54],
            [7, 52],
            [8, 62],
            [9, 59],
            [10, 66],
            [11, 48],
            [12, 42]
	];
	var data2 = [
            [1, 18],
            [2, 23],
            [3, 15],
            [4, 26],
            [5, 19],
            [6, 35],
            [7, 41],
            [8, 46],
            [9, 32],
            [10, 34],
            [11, 31],
            [12, 25]
	];
	
	jq(".chart-placeholder").each(function() {
	    var plot = jq.plot(jq(this), [{
		data: data1,
		label: "2012"
	    }, {
		data: data2,
		label: "2013"
	    }], {
		series: {
		    lines: {
			show: true,
			lineWidth: 1,
			fill: true,
			fillColor: {
			    colors: [{
				opacity: 0.05
			    }, {
				opacity: 0.09
			    }]
			}
		    },
		    points: {
			show: true,
			lineWidth: 2,
			radius: 3
		    },
		    shadowSize: 0,
		    stack: true
		},
		grid: {
		    hoverable: true,
		    clickable: true,
		    tickColor: "#f9f9f9",
		    borderWidth: 0
		},
		legend: {
		    // show: false
		    labelBoxBorderColor: "#fff"
		},
		colors: ["#94aec4", "#3473A9"],
		xaxis: {
		    ticks: [
			[1, "JAN"],
			[2, "FEB"],
			[3, "MAR"],
			[4, "APR"],
			[5, "MAY"],
			[6, "JUN"],
			[7, "JUL"],
			[8, "AUG"],
			[9, "SEP"],
			[10, "OCT"],
			[11, "NOV"],
			[12, "DEC"]
		    ],
		    font: {
			size: 8,
			family: "Open Sans, Arial",
			variant: "small-caps",
			color: "#9da3a9"
		    }
		},
		yaxis: {
		    ticks: 3,
		    tickDecimals: 0,
		    font: {
			size: 8,
			color: "#9da3a9"
		    }
		}
	    });
	});
    }

    /***** END OF PLOTS *****/
    
    /***** START OF NAVIGATION *****/
    
    var navigation = {
	cluster: function(name) {
	    localStorage.setItem('cluster-name', name);
	    window.location.href = ui.base+'/cluster.html';
	    return false;
	},
	project: function(uuid) {
	    localStorage.setItem('project-uuid', uuid);
	    window.location.href = ui.base+'/project.html';
	    return false;
	}
    };

    /***** END OF NAVIGATION *****/
    
    /***** START OF IFRAME LOADERS *****/

    var loaders = {
	project: function() {
	    var uuid = localStorage.getItem('project-uuid');
	    var iframe = jq('.report-frame');
	    
	    iframe.removeAttr('srcdoc', false);
	    iframe.attr('src', '/reports/project/'+uuid+'/latest');

	    iframe.load(function() {
		var page = iframe.contents().find('.page-a4');
		var bounds = page[0].getBoundingClientRect();
		iframe.css('height', bounds.height+2)
	    });
	},
	cluster: function(tab) {
	    var cluster = localStorage.getItem('cluster-name').toLowerCase().replace(/ /g, '-');
	    var iframe = jq('.report-frame');
	    
	    iframe.removeAttr('srcdoc', false);
	    iframe.attr('src', '/reports/cluster/'+cluster+'/latest/'+tab+'/');

	    iframe.load(function() {
		setTimeout(function() {
		    var page = iframe.contents().find('.page-a4');
		    var bounds = page[0].getBoundingClientRect();
		    iframe.css('height', bounds.height+2)
		}, 1000);
	    });
	}
    };

    /***** END OF IFRAME LOADERS *****/
    
    /***** START OF DYNAMIC TAGS *****/

    (function() {
	var cluster = {
	    name: localStorage.getItem('cluster-name')
	}
	var project = {
	    uuid: localStorage.getItem('project-uuid'),
	    name: localStorage.getItem('project-name')
	}
	
	jq('span.pmis-cluster-name').text(cluster.name);
	jq('span.pmis-project-name').text(project.name);
    })();

    /***** END OF DYNAMIC TAGS *****/

    
    /* Public interface. */
    return {
	session: session,
	logout: logout,
	cluster: navigation.cluster,
	project: navigation.project,
	charts: tempcharts,
	navigation: {
	    cluster: navigation.cluster,
	    project: navigation.project
	},
	loaders: {
	    project: loaders.project,
	    cluster: loaders.cluster
	}
    }
})($);
