/*
 * main.js
 */

$(document).ready(function(){
	initRouter();
	checkAuth();
});

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {
			"course/:course_id":	"course",
			"*data" : 				"default"
		},
		
		default: function(data){
			console.log("Hash passed data: "+data);
		},
		
		course: function(course_id){
			console.log("You want to load the course with ID "+course_id);
		}
	});
	
	var router = new Router;
	Backbone.history.start();
}

function checkAuth(){
	$.get('/api/init/get', function(json){
		if(!$.isEmptyObject(json)){
			var src = $('#welcome-template').html();
			var tmpl = Handlebars.compile(src);
			$.extend(json, {uniname: $.cookie('zabeta_uni_name')});
			var html = tmpl(json);
			$('#main').html(html);
		}else{
			initUniPicker();
		}
	});
}

function initUniPicker(){	
	if($.cookie('zabeta_uni_id') != null){
		$.cookie('zabeta_uni_id', $.cookie('zabeta_uni_id'), { expires: 21900});
		$.cookie('zabeta_uni_name', $.cookie('zabeta_uni_name'), {expires: 21900});
		window.location = 'authentication/'+$.cookie('zabeta_uni_id');
		return
	}
	$.get('/api/University/list', function(json){
		var src = $('#uni-template').html();
		var tmpl = Handlebars.compile(src);
		$.extend(json, {heading: 'Please select an institution'});
		var html = tmpl(json);
		$('#main').html(html);
	}).success(function(){
		$('#uni').change(function(){
			var selected = $('#uni option:selected');
			$.cookie('zabeta_uni_id', selected.val(), { expires: 21900});
			$.cookie('zabeta_uni_name', selected.text(), {expires: 21900});
			window.location = '/authentication/'+selected.val();
		});
	});
	

}