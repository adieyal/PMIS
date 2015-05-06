$(document).ready(function() {
    var json = {}
    var templates = {
	slider: [
	    {
		"position": 0.5,
		"bar-color": "#e5b744",
		"marker-color": "#656263",
		"marker-style": "short",
		"marker-text": "Budget"
	    },
	    {
		"position": 0.65,
		"bar-color": "#f04338",
		"marker-color": "#f04338",
		"marker-style": "long",
		"marker-text": "Actual"
	    }
	],
	gauge: [
	    {
		"position": 0.5,
		"text": "Planned",
		"needle-style": "dashed"
	    },
	    {
		"position": 0.85,
		"text": "Actual",
		"needle-color": ["#86bf53", "#cce310"],
		"needle-style": "plain"
	    }
	],
	donut: {
	    "as_percentage" : true,
	    "values" : [0.5, 0.65, 0.35, 0.65]
	}
    }
    $('.replace').each(function() {
	var key = $(this).attr('id');
	var value = $(this).text();
	json[key] = value;
    });
    $('.widget').each(function() {
	var key = $(this).attr('data-src').split('#')[1];
	var widget = $(this).attr('data-widget');
	var value = templates[widget];
	json[key] = value;
    });
    console.log(JSON.stringify(json));
});
