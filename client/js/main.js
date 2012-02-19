/*
 * main.js
 */

$(document).ready(function(){
	initRouter();
	checkAuth();
  loadToolbar();
});

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {
			"course/:course_id":	"course",
      "tasks": "loadTasks",
			"*data" : 				"default"
		},

    loadTasks: function() { loadTasksList(); },

		default: function(data){
			console.log("Hash passed data: "+data);
      $('#container').html('<a href="#tasks">Tasks</a>');
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
		if($.isEmptyObject(json)){
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

function loadToolbar() {
	$.get('/api/init/get', function(json){
		if(!$.isEmptyObject(json)){
			var src = $('#toolbar-tmpl').html();
			var tmpl = Handlebars.compile(src);
			$.extend(json, {usr_logo: 'img/face.png', uni_name:$.cookie('zabeta_uni_name')});
			var html = tmpl(json);
			$('#toolbar').html(html);
		}else{
			initUniPicker();
		}
	});
}

function loadTasksList() {
  var context = {
    "list_title": "Task List",
    "list_header": [
      {"heading":"Title"},
      {"heading":"Type"},
      {"heading":"Priority"},
      {"heading":"State"},
      {"heading":"Responsible"},
      {"heading":"Due by"}],
    "list_row": [
      {"list_row_item":[
        {"list_row_item_data":"Senior Exit Survey"},
        {"list_row_item_data":"Survey"},
        {"list_row_item_data":"Top priority"},
        {"list_row_item_data":"Incomplete"},
        {"list_row_item_data":"Dr. G"},
        {"list_row_item_data":"Today"}]}]
  };
  var source   = $("#list-tmpl").html();
  var template = Handlebars.compile(source);
  $('#container').html(template(context));
}
