(function() {
    $(document).ready(function() {
	var scale = $(window).width() / $(document).width();
	var body = $('body');
	
	body.css('transform', 'scale('+scale+')');
	body.css('transform-origin', '0 0');
	$('html').css('height', '100%');
    });
})();
