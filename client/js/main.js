/*
 * main.js
 */

/* Temporary proof-of-concept var */
var taskListJson;
var formJson;


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
	$.get('/api/state/get', function(json){
		if(!$.isEmptyObject(json['state'])){
			var uni_name;
			$.getJSON('/api/mora/'+json['state']['university'], function(uni_json){
				uni_name = uni_json['name'];
				$.extend(json['state'], {usr_logo: 'img/face.png', uni_name:uni_name});
				console.log(json);
				T.render('toolbar', function(t) {
					 $('#toolbar').html( t(json) );
				});
				loadMenu();
				loadTasksList();
				loadTermCourses();
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
  taskListJson = {
    "list_title": "Tasks Assigned",
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
  updateList();
}

/* Temp proof-of-concept fn */
function addAnotherTask(){
	taskListJson.list_row.push({"list_row_item":[
        {"list_row_item_data":"Senior Exit Survey"},
        {"list_row_item_data":"Survey"},
        {"list_row_item_data":"Top priority"},
        {"list_row_item_data":"Incomplete"},
        {"list_row_item_data":"Dr. G"},
        {"list_row_item_data":"Today"}]});
	updateList();
}

/* Temp proof-of-concept fn */
function updateList(){
	T.render('list', function(t) {
		 $('#top').html( t(taskListJson) );
	});
}

function loadCourseData(course_id){
	$.getJSON('/api/mora/'+course_id, function(json){
		T.render('course', function(t) {
			 $('#top').html( t(json) );
		});
	});
}

function loadTermCourses(){
	termcourseJson = {
			"Semester":[
			            {"name":"Semester Name"}
			           ],
			 "CourseOffering":[
			                   {"name": "Automata Theory", "catalog": "CS 315"},
			                   {"name": "Computer Science I ", "catalog": "CS 126"}
			                  ]
	}
	T.render('term_class_list', function(t){
		$('#bottom-left').html(t(termcourseJson));
	});
}
