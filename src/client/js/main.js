/*
 * main.js
 *
 */

$(document).ready(function(){
	initRouter();
	initPage();
});

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {
			"course/:course_id":	"course",
			"users":				"users",
			"programs":				"programs",
			"allTasks":				"allTasks",
			"accredidation":		"accredidation",
			"uploadTest":			"uploadTest",
			"*data": 				"default"
		},

		default: function(data){
			clearPanes();
			loadDashboard();
			embolden('#overview');
		},

		course: function(course_id){
			clearPanes();
			loadCourseData(course_id);
		},

		users: function(){
			clearPanes();
			loadUsers('#top');
			embolden('#users');
		},

		programs: function(){
			clearPanes();
			loadProgramList();
			embolden('#programs');
		},

		allTasks: function() {
			clearPanes();
			collapsePanes();
			loadAllTasksPage('#top');
			embolden('#allTasks')
		},

		accredidation: function(){
			clearPanes();
			loadAccredationPage('#top');
			embolden('#accredidation');
		},

		uploadTest: function(){
			clearPanes();
			loadUploadPage();
			embolden('#uploadTest');
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
				login_path = uni_json['login_path'];
				$.jStorage.set('login_path', login_path);
				$.jStorage.setTTL('login_path', 604800000);
				$.extend(json['user'], {usr_logo: 'img/face.png', uni_name:uni_name});
				T.render('toolbar', function(t) {
					 $('#toolbar').html( t(json) );
				});
				loadProgramChooser();
			});
		}
	});
}

function loadProgramChooser(){
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
						var program = $('#program-chooser-select option:selected').val();
						$.jStorage.set('program', program);
						updateProgramToolbar(program);
						$.cookie('program', program, { expires: 7});
						$.jStorage.setTTL('program', 604800000);
					}else{
						$('#program-chooser-select').val($.jStorage.get('program'));
					}
					$('#program-chooser-select').change(function(){
						var program = $('#program-chooser-select option:selected').val();
						$.jStorage.set('program', program);
						updateProgramToolbar(program);
						$.cookie('program', program, { expires: 7});
						$.jStorage.setTTL('program', 604800000);
						updateProgramToolbar(program);
						loadMenu();
					});
					loadMenu();
				});
			}
		});
	}else{
		var program = userdata['user']['programs'][0];
		$.jStorage.set('program', program);
		updateProgramToolbar(program);
		$.cookie('program', program, { expires: 7});
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
					"hash": "accredidation",
					"name":	"Accredidation"
				},
				{
					"hash": "uploadTest",
					"name": "Test Upload"
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
						"hash": "allTasks",
						"name":	"All Tasks"
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
	T.render('menu', function(t) {
		 $('#menu-content').html( t(menuJson) );
	});
}

function loadCourseData(course_id){
	$.getJSON('/api/crud/'+course_id, function(json){
		T.render('course', function(t) {
			 $('#top').html( t(json) );
		});
	});
}

function loadAllTasksPage(element) {
	$.getJSON('/api/list/Task/', function(json) {
		for(var key in json['Task']){
			var end_date = json['Task'][key]['end_date'];
			var relative_date = getRelativeDate(end_date);
			$.extend(json['Task'][key], {'relative_date': relative_date});
		}
		T.render('all_tasks', function(t) {
			$(element).html( t(json) );
		});
	});
}

function loadAccredationPage(element){
	collapsePanes();
	$.getJSON('/api/list/Objective', function(json){
		console.log(json);
		T.render('objective_list', function(t){
			$(element).html(t(json));
		});
	});
}

function loadTasks(element){
	  $.getJSON('api/user/getTasks', function(json){
		    for(var key in json['user']){
				var end_date = json['user'][key]['end_date'];
				var relative_date = getRelativeDate(end_date);
				$.extend(json['user'][key], {'relative_date': relative_date});
			}
			T.render('task_list', function(t) {
				 $(element).html( t(json) );
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

function loadPrograms(element){
	$.getJSON('api/list/Program', function(programJSON){
		T.render('program_list', function(t){
			$(element).html(t(programJSON));
		});
	});
}

function loadProgramList(){
	expandPanes();
	loadPrograms('#top');
	loadUsers('#bottom-left');
	//loadTermCourses('#bottom-right');
}

function loadDashboard() {
	expandPanes();
	loadTasks('#top');
	loadTermCourses('#bottom-left');
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

Handlebars.registerHelper('taskResponse', function(response, options) {
	var ret = ''
	console.log('Response: ');
	console.dir(response);
	if (response == 'None') return '';
	ret += options.fn();
  return ret;
});

function view(id, template){
	$.getJSON('/api/crud/'+id, function (json) {
		/* get referenced properties
		   $.ajax({
		    	type: 'POST',
		    	url: 'api/list/Batch',
		    	dataType: 'json',
		    	data: {
		    	},
		    	success: function (references) {
		    	}
		   });
		*/

		T.render(template, function (t) {
			var data = {
				view: true,
				task: json
			};
			$('#dialog').dialog({
				title: 'View',
				minWidth: 580,
				/*
					TODO: Obviously this is fragile!
					      What should happen is the dialog should expand to display
					      its contents, until a maximum then overflow-y: scroll
								its contents.
					header: 32
					body: (6*42)
					actions: 42
				*/
				minHeight: 32 + 42 + (6*42)
			});
			$('#dialog').html(t(data));
		});
	});
}

function edit(id, template){
	$('#dialog').dialog({
		title: 'Edit',
		minWidth: 580,
		minHeight: 560
	});
	$.getJSON('/api/crud/'+id, function (json) {
		T.render(template, function (t) {
			var data = {
				edit: true,
				task: json
			};
			$('#dialog').html(t(data));
		});
	});
}

function addNew(type){
	$('#dialog').dialog({
		'title': 'Add'
	});
	$('#dialog').html('This is a box where you would add a new <strong>'+type+'</strong>');
}

function editResponse(id, template) {
	$('#edit-response').dialog({
		title: 'Edit',
		minWidth: 1020,
		minHeight: 750
	});

	$.getJSON('/api/crud/'+id, function (json) {
		T.render(template, function (t) {
			$('#edit-response').html(t(json));

			var input = $('#source');
			var demo = document.getElementById('generated');

			var creole = new WikiForms.Form({
				forIE: document.all,
				interwiki: {
					WikiCreole: 'http://www.wikicreole.org/wiki/',
					Wikipedia: 'http://en.wikipedia.org/wiki/'
				},
				linkFormat: ''
			});

			var render = function () {
				demo.innerHTML = '';
				creole.parse(demo, input.val());
			};

			$('#build').click(function () {
				render();
			});

			$('#update-response').click(function () {
				$.ajax({
					type: 'POST',
					url: '/api/crud/'+id+'/response',
					data: input.val()
				});
			});
		});
	});
}

function getRelativeDate(abs_date){
	$('#relativeTimeHandler').remove();
	$('body').append('<div id="relativeTimeHandler" style="display:none"></div>');
	$('#relativeTimeHandler').attr('datetime', abs_date);
	$('#relativeTimeHandler').html('');
	$('#relativeTimeHandler').relative({format:'human', displayZeros:false, tick:0	});
	return $('#relativeTimeHandler').html();
}

function embolden(element){
	$('.menu-item').each(function(){
		$(this).css('font-weight', 'normal');
	});
	$(element).css('font-weight', 'bold');
}

function updateProgramToolbar(program){
	$.getJSON('/api/crud/'+program, function(json){
		$('#program').html('&nbsp;-&nbsp;'+json['description']);
	});
}
