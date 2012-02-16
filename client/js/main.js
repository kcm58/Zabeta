/*
 * main.js
 */

$(document).ready(function(){
	initRouter();
	initUniPicker();
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

function initUniPicker(){	
	$.get('/api/University/list', function(json){
		var src = $('#uni-template').html();
		var tmpl = Handlebars.compile(src);
		var html = tmpl(json);
		$('#main').html(html);
	}).success(function(){
		$('#uni').change(function(){
			var selected = $('#uni option:selected').val();
			$.cookie('zaba_uni_id', selected, { expires: 21900});
			window.location = '/authentication/'+selected;
		});
	});
	

}