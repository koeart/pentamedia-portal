function setupStars(stars) {
    var origText = stars.text();
    var origStyle = stars.attr('style');
    var hovering = false;
    var form_loaded = false;
    var curText;

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
        icon.mouseover((function(j) {return function() {
            var k;
            for(k = 1; k <= j; k++)
            icons[k].text('★');
            for(k = j + 1; k < 6; k++)
            icons[k].text('☆');
        }})(i));
        icon.click((function(j) {return function() {
            curText = stars.text();
            if (form_loaded) {
                $('#rating-score').val(j);
                return;
            }
            form_loaded = true;
            var rateUrl = $('.add_rating').attr('href');
            $.get(rateUrl, function(data) {
                var form = $(data).find('#new');
                form.find('p.scores').remove();
                form.append('<input type="hidden" name="score" ' +
                            'id="rating-score" value="' + j + '"/>');
                stars.after(form);
            });
        }})(i));
        stars.append(icon);
    }
    });
    stars.mouseleave(function() {
        hovering = false;
        stars.children().remove();
        if (form_loaded) {
           stars.text(curText);
           return;
        }
        stars.text(origText);
        stars.attr('style', origStyle);
    });
}

$('.stars').each(function() {
    setupStars($(this));
});