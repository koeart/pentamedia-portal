function mergeFormsets() {
    var fieldsets = $('fieldset.captcha');
    var shit = $('<fieldset><legend></legend><div></div></fieldset>');
    fieldsets.last().after(shit);

    var panes = {};
    fieldsets.each(function() {
	$(this).detach();
	var legend = $(this).find('legend');
	panes[legend.find('input').val()] = $(this).contents();

	legend.detach();
	shit.find('legend').append(legend.contents());
    });

	/*var tab = legend.find('input');
console.log({tab:tab})
	tab.select(function() {
console.log('select')
	    var content = shit.find('div');
	    content.empty();
	    content.append(this);
	});*/

    var switchPane = function() {
	var content = shit.find('div');
	content.empty();
	shit.find('legend input').each(function() {
	    if (this.checked) {
		content.append(panes[$(this).val()]);
	    }
	});
    };

    shit.find('input').change(function() {
	switchPane();
    });
    switchPane();
}

/* No need for $(document).ready(), <script/> sits at the bottom of body */
mergeFormsets();
