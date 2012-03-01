/*
 * main.js
 */


$(document).ready(function(){
	initRouter();
	initPage();
});

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {		
			"course/:course_id":	"course",
			"*data": 				"default"
		},

		default: function(data){
			
		},

		course: function(course_id){
			loadCourseData(course_id);
		},
			
	});

	var router = new Router;
	Backbone.history.start();
}


function initPage() {
	$.get('/api/user/get', function(json){
		if(!$.isEmptyObject(json['user'])){
			var uni_name;
			$.getJSON('/api/crud/'+json['user']['university'], function(uni_json){
				uni_name = uni_json['name'];
				$.extend(json['user'], {usr_logo: 'img/face.png', uni_name:uni_name});
				T.render('toolbar', function(t) {
					 $('#toolbar').html( t(json) );
				});
				loadMenu();
				loadTasksList();
				loadTermCourses();
				loadProgramList();
			});
		}
	})
	.error(function(){$('#top').html('<img src="img/google-signin.png" alt="Sign in with Google" />');});
}

function loadMenu(){
	menuJson = {
			"items":
				[{
					"hash":	"overview",
					"name":	"Overview"
				},
				{
					"hash":	"program",
					"name":	"Program"
				},
				{
					"hash": "accredidation",
					"name":	"Accredidation"
				}]
	}
	T.render('menu', function(t) {
		 $('#menu-content').html( t(menuJson) );
	});
	if(window.location.hash.indexOf('course') != -1){
		loadCourseList();
	}
}

function loadTasksList() {
  $.getJSON('api/user/getTasks', function(json){
    for(var key in json['user']){
    	$('body').append('<div id="relativeTimeHandler" style="display:none"></div>');
		var end_date = json['user'][key]['end_date'];
		var endDateTicks = Date.parse(end_date);
		$('#relativeTimeHandler').attr('datetime', end_date);
		$('#relativeTimeHandler').html('');
		var format;
		if(new Date().getTime() > endDateTicks){
			format = '%dd %DAYS ago';
		}else{
			format = 'in %dd %DAYS';
		}
		$('#relativeTimeHandler').relative({format:format, displayZeros:false, tick:0	});
		var relative_date = $('#relativeTimeHandler').html();
		$.extend(json['user'][key], {'relative_date': relative_date});
		$('#relativeTimeHandler').remove();
	}
	T.render('task_list', function(t) {
		 $('#top').html( t(json) );
	});
  });
}

function loadCourseData(course_id){
	$.getJSON('/api/crud/'+course_id, function(json){
		T.render('course', function(t) {
			 $('#top').html( t(json) );
		});
	});
}

function loadTermCourses(){
	var outputJSON = {};
	$.getJSON('/api/list/Semester', function(json){
		$.extend(outputJSON, {'semester_name': json['Semester'][0]['name']});
	});
	$.getJSON('/api/user/getCurrentCourses', function(json){
		$.extend(outputJSON, json);
	});
	T.render('term_class_list', function(t){
		$('#bottom-left').html(t(outputJSON));
	});
}

function loadProgramList(){
	$.getJSON('api/user/get', function(json){
		if(json['user']['programs'].length > 1){
			$('#program-chooser').html('<select id=\"program-chooser-select\"></select>');
			var programListJSON = {'programs': []};
			for(i in json['user']['programs']){
				$.getJSON('api/crud/'+json['user']['programs'][i], function(json){
					$('#program-chooser-select').append('<option value="'+json['id']+'">'+json['name']+'</option>');
				});
			}	
		}
	});
}
