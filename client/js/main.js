/*
 * main.js
 */


$(document).ready(function(){
	initRouter();
	initPage();
	/* 
	 * Hides the loading pane when all AJAX requests are done
	 * alaxComplete recieves a callback whenever an AJAX request finishes
	 * and $.active is the number of active AJAX requests
	 * ...not sure why but 1 is the lowest it gets.
	 * 
	 * It also will SHOW the loading screen whenever any AJAX requests occur.
	 * We can tone down what it looks like if it's too intrusive, popping up too much
	 */
	$('body').ajaxStop(function(){
		$('#loading').hide();
	});
	$('body').ajaxStart(function(){
		$('#loading').show();
	});
});

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {		
			"course/:course_id":	"course",
			"users":				"users",
			"*data": 				"default"
		},

		default: function(data){
			loadDashboard();
		},

		course: function(course_id){
			loadCourseData(course_id);
		},
		
		users: function(){
			loadUsers();
		}
			
	});

	var router = new Router;
	Backbone.history.start();
}


function initPage() {
	$.getJSON('/api/user/get', function(json){
		$.jStorage.set('userdata', json);
		if(!$.isEmptyObject(json['user'])){
			var uni_name;
			$.getJSON('/api/crud/'+json['user']['university'], function(uni_json){
				uni_name = uni_json['name'];
				$.extend(json['user'], {usr_logo: 'img/face.png', uni_name:uni_name});
				T.render('toolbar', function(t) {
					 $('#toolbar').html( t(json) );
				});
				loadProgramList();
			});
		}
	})
	.error(function(){
		$('#top').html('<img src="img/google-signin.png" alt="Sign in with Google" />');
	});
}

function loadProgramList(){
	var userdata = $.jStorage.get('userdata');
	if(userdata['user']['programs'].length > 1){
		$('#program-chooser').html('');
		var programsStore = {programs: []};
		for(key in userdata['user']['programs']){
			$.ajax({
				url: 'api/crud/'+userdata['user']['programs'][key],
				dataType: 'json',
				ajaxKey: key,
				success: function(programjson){
					key = this.ajaxKey;
					programsStore['programs'][key] = {programName: programjson['name'], programId: programjson['id']}
					if(key == userdata['user']['programs'].length-1){
						T.render('program_chooser', function(t){
							$('#program-chooser').html(t(programsStore));
							///////// REMOVE ME IN FINAL RELEASE /////////
							$.jStorage.deleteKey('program');
							///////// 			 THANKS		 	 /////////  
							if($.jStorage.get('program') == null){
								$.jStorage.set('program', $('#program-chooser-select option:selected').val());
								$.jStorage.setTTL('program', 604800000);
							}else{
								$('#program-chooser-select').val($.jStorage.get('program'));
							}
							$('#program-chooser-select').change(function(){
								$.jStorage.set('program', $('#program-chooser-select option:selected').val());
								$.jStorage.setTTL('program', 604800000);
								loadMenu();
							});
						});
						loadMenu();
					}
				}
			});
		}	
	}else{
		$.jStorage.set('program', json['user']['programs'][0]);
		$.jStorage.setTTL('program', 604800000);
	}
}

function loadMenu(){
	var programID = $.jStorage.get('program');
	var privilege = 0;
	var userdata = $.jStorage.get('userdata');
	var programIndex = $.inArray(programID, userdata['user']['programs']);
	privilege = userdata['user']['privileges'][programIndex];
	var menuJson = {
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
	if(privilege == 2){
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
					},
					{
						"hash": "tasks",
						"name":	"Tasks"
					},
					{
						"hash": "users",
						"name":	"Users"
					}]
		}
	}
	$.getJSON('/api/crud/'+programID, function(data){
		$.extend(menuJson, data);
		T.render('menu', function(t) {
			 $('#menu-content').html( t(menuJson) );
		});
	});
}

function loadDashboard() {
  expandPanes();
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
	loadTermCourses();
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
		var inAjax = false;
		for(var key in json['user']){
			var courseID = json['user'][key]['course'];
			$.ajax({
				url: 'api/crud/'+courseID,
				dataType: 'json',
				ajaxKey: key,
				success: function(coursejson){
					key = this.ajaxKey;
					$.extend(json['user'][key], {name: coursejson['name'], catalog: coursejson['catalog']});
					if(key == json['user'].length-1){
						$.extend(outputJSON, json);
						T.render('term_class_list', function(t){
							$('#bottom-left').html(t(outputJSON));
						});
					}
				}
			});
		}
	});
}

function collapsePanes(){
	$('#bottom-left').hide();
	$('#bottom-right').hide();
	$('#top').css('height', '100%');
	$('#top').css('border', 0);
}

function expandPanes(){
	$('#bottom-left').show();
	$('#bottom-right').show();
	$('#top').css('height', '');
	$('#top').css('border-bottom', '1px gray dashed');
}

function loadUsers(){
	var userdata = $.jStorage.get('userdata');
	collapsePanes();
	$.getJSON('api/list/User', function(userJSON){
		T.render('user_list', function(t){
			$('#top').html(t(userJSON));
		})
	});
}