

function onload_function(){
	'use strict';
	
	var a_obj, mato_txt, ma_txt, at_txt, ext_txt, all_txt;
	
	// build addresses
	ma_txt = "andre-zanchetta";
	at_txt = "uiowa";
	ext_txt = "edu"
	all_txt = ma_txt + "@" + at_txt + "." + ext_txt;
	mato_txt = "ma" + "il" + "to:" + all_txt;
	
	// fill object
	a_obj = $('#contact_mail');
	a_obj.attr("href", mato_txt)
	a_obj.html(all_txt);
}
