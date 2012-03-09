/*
 * main.js
 */

//This is used to display a message to the user if something goes wrong while loading the page
var loadingTimeout;

$(document).ready(function(){
	initRouter();
	initPage();
	clearTimeout(loadingTimeout);
	loadingTimeout = setTimeout("showLoadingHelp()", 5000);
	$('#loading').show();
	/*
	 * Hides the loading pane when all AJAX requests are done
	 * ajaxStop receives a callback whenever an AJAX request finishes
	 * and there are no active AJAX requests left
	 *
	 * It also will SHOW the loading screen whenever any AJAX requests occur.
	 * We can tone down what it looks like if it's too intrusive, popping up too much
	 */
	$('body').ajaxStop(function(){
		clearTimeout(loadingTimeout);
		$('#loading').hide();

	});
	$('body').ajaxStart(function(){
		clearTimeout(loadingTimeout);
		loadingTimeout = setTimeout("showLoadingHelp()", 5000);
		$('#loading').show();
	});
});

function showLoadingHelp(){
	$('#loading-text').html('<h1>Loading...</h1><h3>This is taking longer than usual...soemthing may have gone wrong.</h3><img src="img/ajax-loader.gif" />')
}

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {
			"course/:course_id":	"course",
			"users":				"users",
			"programs":				"programs",
			"tasks":				"tasks",
			'allTasks':			"allTasks",
			"uploadTest":			"uploadTest",
			"*data": 				"default"
		},

		default: function(data){
			clearPanes();
			loadDashboard();
		},

		course: function(course_id){
			clearPanes();
			loadCourseData(course_id);
		},

		users: function(){
			clearPanes();
			loadUsers('#top');
		},

		programs: function(){
			clearPanes();
			loadPrograms();
		},

		tasks: function(){
			clearPanes();
			loadTaskPage();
		},

		allTasks: function() {
			clearPanes();
			loadAllTasksPage();
		},

		uploadTest: function(){
			clearPanes();
			loadUploadPage();
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
		$.ajax({
			url: 'api/list/Batch',
			dataType: 'json',
			data: JSON.stringify(userdata['user']['programs']),
			type: "POST",
			success: function(json){
				for(var key in json['Batch']){
					programsStore['programs'][key] = {programName: json['Batch'][key]['name'], programId: json['Batch'][key]['id']};
				}
				T.render('program_chooser', function(t){
					$('#program-chooser').html(t(programsStore));
					///////// REMOVE ME IN FINAL RELEASE /////////
					$.jStorage.deleteKey('program');
					///////// 			 THANKS		 	 ////////
					if($.jStorage.get('program') == null){
						$.jStorage.set('program', $('#program-chooser-select option:selected').val());
						$.cookie('program', $('#program-chooser-select option:selected').val(), { expires: 7});
						$.jStorage.setTTL('program', 604800000);
					}else{
						$('#program-chooser-select').val($.jStorage.get('program'));
					}
					$('#program-chooser-select').change(function(){
						$.jStorage.set('program', $('#program-chooser-select option:selected').val());
						$.cookie('program', $('#program-chooser-select option:selected').val(), { expires: 7});
						$.jStorage.setTTL('program', 604800000);
						console.log($.jStorage.get('program'));
						loadMenu();
					});
					loadMenu();
				});
			}
		});
	}else{
		$.jStorage.set('program', userdata['user']['programs'][0]);
		$.cookie('program', userdata['user']['programs'][0], { expires: 7});
		$.jStorage.setTTL('program', 604800000);
		console.log($.jStorage.get('program'));
		loadMenu();
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
					"hash":	"programs",
					"name":	"Programs"
				},
				{
					"hash": "accredidation",
					"name":	"Accredidation"
				},
				{
<<<<<<< HEAD
					'hash': 'allTasks',
					'name': 'All Tasks'
=======
					"hash": "uploadTest",
					"name": "Test Upload"
>>>>>>> 7cd42415543a6c20dad2448ce23c35fc68634c6b
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
						"hash":	"programs",
						"name":	"Programs"
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
					},
					{
						"hash": "uploadTest",
						"name": "Test Upload"
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

function loadCourseData(course_id){
	$.getJSON('/api/crud/'+course_id, function(json){
		T.render('course', function(t) {
			 $('#top').html( t(json) );
		});
	});
}

function loadTasks(element){
  $.getJSON('api/user/getTasks', function(json){
	    for(var key in json['user']){
	    	$('body').append('<div id="relativeTimeHandler" style="display:none"></div>');
			var end_date = json['user'][key]['end_date'];
			var endDateTicks = Date.parse(end_date);
			$('#relativeTimeHandler').attr('datetime', end_date);
			$('#relativeTimeHandler').html('');
			$('#relativeTimeHandler').relative({format:'human', displayZeros:false, tick:0	});
			var relative_date = $('#relativeTimeHandler').html();
			$.extend(json['user'][key], {'relative_date': relative_date});
			$('#relativeTimeHandler').remove();
		}
		T.render('task_list', function(t) {
			 $(element).html( t(json) );
		});
	  });
}

function loadAllTasksPage() {
	$.getJSON('/api/list/Task/', function(json) {
		T.render('all_tasks', function(t) {
			 $('#top').html( t(json) );
		});
	});
}

function loadTermCourses(element){
	var outputJSON = {};
	$.getJSON('/api/list/Semester', function(json){
		$.extend(outputJSON, {'semester_name': json['Semester'][0]['name']});
	});
	$.getJSON('/api/user/getCurrentCourses', function(json){
		//prepare a list of IDs
		var courseIDs = [];
		for(var key in json['user']){
			courseIDs[key] = json['user'][key]['course'];
		}
		$.ajax({
			url: 'api/list/Batch',
			dataType: 'json',
			data: JSON.stringify(courseIDs),
			type: "POST",
			success: function(json){
				$.extend(outputJSON, json);
				T.render('term_class_list', function(t){
					$(element).html(t(outputJSON));
				});
			}
		});
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

function clearPanes(){
	$('#top').html('');
	$('#bottom-left').html('');
	$('#bottom-right').html('');
}

function loadUsers(element){
	console.log('hi)');
	var userdata = $.jStorage.get('userdata');
	if(userdata == null){
		initPage();
		userdata = $.jStorage.get('userdata');
	}
	if(element == '#top'){
		collapsePanes();
	}
	$.getJSON('api/list/User', function(userJSON){
		T.render('user_list', function(t){
			$(element).html(t(userJSON));
		});
	});
}

function loadSemesters(element){
	$.getJSON('api/list/Semester', function(semesterJSON){
		console.log(semesterJSON);
		T.render('semester_list', function(t){
			$(element).html(t(semesterJSON));
		});
	});
}

function loadPrograms(){
	expandPanes();
	loadSemesters('#top');
	loadUsers('#bottom-left');
	loadTermCourses('#bottom-right');
}

function loadDashboard() {
	expandPanes();
	loadTasks('#top');
	loadTermCourses('#bottom-left');
}

function loadTaskPage(){
	collapsePanes();
	loadTasks('#top');
}

function loadUploadPage(){
	collapsePanes();
	var json = {}
	var userdata = $.jStorage.get('userdata');
	var id = userdata['user']['id'];
	$.extend(json, {'id': id});
	T.render('upload_test', function(t){
		$('#top').html(t(json));
		$.getJSON('file/getAll', function(fileJSON){
			for(var key in fileJSON){
				$('#top').append('<a href="file/download/'+fileJSON[key]+'">Uploaded File #'+key+'</a><br />')
			}
		})
		.error(function(jqXHR, textStatus, errorThrown){ alert(textStatus)});
	});
}

//These are development functions that need to be replaced or expanded on
function edit(id, template){
	$('#dialog').dialog({
		title: 'Edit',
		minWidth: 340,
		minHeight: 480
	});
	$.getJSON('/api/crud/'+id, function (json) {
		T.render(template, function (t) {
			 $('#dialog').html(t(json));
		});
	});
}

function addNew(type){
	$('#dialog').dialog({
		'title': 'Add'
	});
	$('#dialog').html('This is a box where you would add a new <strong>'+type+'</strong>');
}
