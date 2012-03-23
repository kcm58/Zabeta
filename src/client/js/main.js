/*
 * main.js
 *
 */

//This is used to display a message to the user if something goes wrong while loading the page
var loadingTimeout;

$(document).ready(function(){
	clearTimeout(loadingTimeout);
	loadingTimeout = setTimeout("showLoadingHelp()", 5000);
	$('#loading').show();
	initRouter();
	initPage();
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
		$('#loading-text').html('<h1>Loading...</h1><img src="img/ajax-loader.gif" />');
		loadingTimeout = setTimeout("showLoadingHelp()", 5000);
		$('#loading').show();
	});
	
	/*
	 * Handle all AJAX errors by assuming the user isn't logged in. Bad, but for now, good.
	 */
	$('body').ajaxError(function(e, jqxhr, settings, exception){
		clearPanes();
		$('#menu').html('');
		$('#toolbar').html('');
		$('#top').html('<img src="img/google-signin.png" alt="Sign in with Google" /><h3>Debug: See JavaScript Console for more info');
		console.log('---Start AJAX Error Details---');
		console.log('Event:');
		console.log(e);
		console.log('jqXHR:');
		console.log(jqxhr);
		console.log('AJAX Settings:');
		console.log(settings);
		console.log('AJAX Exception:');
		console.log(exception);
		console.log('----End AJAX Error Details----');
		console.log();
		console.log();
	});
});

function showLoadingHelp(){
	$('#loading-text').html('<h1>Loading...</h1><img src="img/ajax-loader.gif" /><h3>This is taking longer than usual...soemthing may have gone wrong.</h3>')
}

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {
			"course/:course_id":	"course",
			"users":				"users",
			"programs":				"programs",
			"allTasks":				"allTasks",
			"accredidation":		"accredidation",
			"uploadTest":			"uploadTest",
			"minutes":				"minutes",
			"schedulelog":			"schedulelog",
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
			loadProgramList();
		},

		allTasks: function() {
			clearPanes();
			collapsePanes();
			loadAllTasksPage('#top');
		},

		accredidation: function(){
			clearPanes();
			loadAccredationPage('#top');
		},
		
		minutes: function(){
			clearPanes();
		},
		
		schedulelog: function(){
			clearPanes();
			loadScheduleLog('#top');
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
					//$.jStorage.deleteKey('program');
					///////// 			 THANKS		 	 ////////
					if($.jStorage.get('program') == null){
						var program = $('#program-chooser-select option:selected').val();
						$.jStorage.set('program', program);
						$.cookie('program', program, { expires: 7});
						$.jStorage.setTTL('program', 604800000);
						updateProgramToolbar(program);
					}else{
						$('#program-chooser-select').val($.jStorage.get('program'));
					}
					$('#program-chooser-select').change(function(){
						var program = $('#program-chooser-select option:selected').val();
						$.jStorage.set('program', program);
						$.cookie('program', program, { expires: 7});
						$.jStorage.setTTL('program', 604800000);
						updateProgramToolbar(program);
						var curHash = window.location.hash;
						window.location.hash="";
						window.location.hash = curHash;
						loadMenu();
					});
					loadMenu();
				});
			}
		});
	}else{
		var program = userdata['user']['programs'][0];
		$.jStorage.set('program', program);
		$.cookie('program', program, { expires: 7});
		$.jStorage.setTTL('program', 604800000);
		updateProgramToolbar(program);
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
					"hash":	"",
					"name":	"Overview"
				},
				{
					"hash": "accredidation",
					"name":	"Accredidation"
				},
				{
					"hash": "minutes",
					"name":	"Minutes"
				},]
	}
	if(privilege == 2){
		menuJson = {
				"items":
					[{
						"hash":	"",
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
						"hash": "minutes",
						"name":	"Minutes"
					},
					/*{
						"hash": "allTasks",
						"name":	"All Tasks"
					},*/
					{
						"hash": "users",
						"name":	"Users"
					},
					{
						"hash":	"schedulelog",
						"name": "Schedule Log"
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
	$.getJSON('/api/list/Objective', function(objectivesJSON){
		var outputJSON = objectivesJSON;
		for(var key in objectivesJSON['Objective']){
			$.ajax({
				url: 'api/list/Batch',
				dataType: 'json',
				data:JSON.stringify(objectivesJSON['Objective'][key]['outcomes']),
				type: "POST",
				ajaxKey: key,
				success: function(outcomesJSON){
					var ajaxKey = this.ajaxKey;
					$.extend(outputJSON['Objective'][ajaxKey], outcomesJSON);
					if(ajaxKey == objectivesJSON['Objective'].length-1){
						T.render('objective_list', function(t){
							$(element).html(t(outputJSON));
						});
					}
				}
			});
		}
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
	$.getJSON('api/list/Semester', function(json){
		if(undefined == json['Semester'][0]){
			$.extend(outputJSON, {semester_name: 'fall'});
		}else{
			$.extend(outputJSON, {'semester_name': json['Semester'][0]['name']});
		}
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

function updateProgramToolbar(program){
	$.getJSON('/api/crud/'+program, function(json){
		$('#program').html('&nbsp;-&nbsp;'+json['description']);
	});
}

function loadTOS(){
	$.get('legal/tos.html', function(tos){
		$('#dialog').html(tos);
		$('#dialog').dialog({
			title: 'Terms of Service',
			minWidth: 580,
			minHeight: 560
		});
	});
}

function loadPriv(){
	$.get('legal/privacy.html', function(privacy){
		$('#dialog').html(privacy);
		$('#dialog').dialog({
			title: 'Privacy Policy',
			minWidth: 580,
			minHeight: 560
		});
	});
}

function loadScheduleLog(element){
	$.getJSON('/api/list/ScheduleLog', function(scheduleJSON){
		var tasks = [];
		var users = [];
		for(var key in scheduleJSON['ScheduleLog']){
			tasks[key] = scheduleJSON['ScheduleLog'][key]['task'];
			users[key] = scheduleJSON['ScheduleLog'][key]['user'];
		}
		var tasks_human = [];
		var users_human = [];
		$.ajax({
			url: 'api/list/Batch',
			dataType: 'json',
			data:JSON.stringify(tasks),
			type: "POST",
			success: function(tasksJSON){
				for(var key in tasksJSON['Batch']){
					tasks_human[key] = tasksJSON['Batch'][key];
				}
				$.ajax({
					url: 'api/list/Batch',
					dataType: 'json',
					data:JSON.stringify(users),
					type: "POST",
					success: function(usersJSON){
						for(var key in usersJSON['Batch']){
							users_human[key] = usersJSON['Batch'][key];
						}
						for(var key in scheduleJSON['ScheduleLog']){
							$.extend(scheduleJSON['ScheduleLog'][key], {task_human: tasks_human[key]});
							$.extend(scheduleJSON['ScheduleLog'][key], {user_human: users_human[key]});
						}
						T.render('schedule_log_list', function(t) {
							 $(element).html( t(scheduleJSON) );
						});
					}
				});
			}
		});
	});
}