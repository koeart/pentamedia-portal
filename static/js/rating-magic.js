function setupStars(stars) {
    var origText = stars.text();
    var origStyle = stars.attr('style');
    var hovering = false;

    stars.mouseenter(function() {
	if (hovering)
	    return;
	hovering = true;

	stars.attr('style', 'margin-top:-1em;');
	stars.text('');

	var icons = [], i;
	for(i = 1; i < 6; i++) {
	    var icon = $('<p>☆</p>');
	    icons[i] = icon;
	    icon.mouseover((function(j) {
		return function() {
console.log('mouseover: '+j);
		    var k;
		    for(k = 1; k <= j; k++)
			icons[k].text('★');
		    for(k = j + 1; k < 6; k++)
			icons[k].text('☆');
		};
	    })(i));
	    icon.click((function(j) {
		return function() {
console.log('click: '+j);
		    var rateUrl = $('.add_rating').attr('href');
console.log('rateUrl: '+rateUrl);
		    $.get(rateUrl, function(data) {
			var form = $(data).find('#new');
			form.find('p.scores').remove();
			form.append('<input type="hidden" name="score" value="' +
				    j +
				    '"/>');
			stars.after(form);
			/*document.write('<script src="/js/captcha-form.js" type="application/javascript"></script>');*/
		    });
		};
	    })(i));
	    stars.append(icon);
	}
    });
    stars.mouseleave(function() {
	stars.children().remove();
	stars.text(origText);
	stars.attr('style', origStyle);
	hovering = false;
    });
}

$('.stars').each(function() {
    setupStars($(this));
});