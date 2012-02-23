/*
 * main.js
 */

/* Temporary proof-of-concept var */
var taskListJson;
var formJson;


$(document).ready(function(){
	initRouter();
	checkAuth();
	
});

function initRouter(){
	var Router = Backbone.Router.extend({
		routes: {		
			"course":				"courseList",
			"course/:course_id":	"course",
			"tasks": 				"loadTasks",
			"form":					"loadForm",
			"*data": 				"default"
		},

		default: function(data){
			console.log("Hash passed data: "+data);
		},

		course: function(course_id){
			loadCourseData(course_id);
		},
		
		courseList: function(){
			$('#course-sub').html('');
			loadCourseList();
		},
		
		loadTasks: function(){
			$('#course-sub').html('');
			loadTasksList();
		},
		
		loadForm: function(){
			$('#course-sub').html('');
			loadForm();
		}
	});

	var router = new Router;
	Backbone.history.start();
}

function checkAuth(){
	$.get('/api/init/get', function(json){
		if($.isEmptyObject(json['init'])){
			initUniPicker();
		}else{
			loadToolbar();
			loadMenu();
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
		var src = $('#uni-tmpl').html();
		var tmpl = Handlebars.compile(src);
		$.extend(json, {heading: 'Please select an institution'});
		var html = tmpl(json);
		$('#content').html(html);
	}).success(function(){
		$('#uni').change(function(){
			var selected = $('#uni option:selected');
			$.cookie('zabeta_uni_id', selected.val(), { expires: 21900});
			$.cookie('zabeta_uni_name', selected.text(), {expires: 21900});
			window.location = '/authentication/'+selected.val();
		});
	});
	$('#content').html('Please go to your special Zabeta URL for your institution');

}

function loadToolbar() {
	$.get('/api/init/get', function(json){
		if(!$.isEmptyObject(json['init'])){
			var src = $('#toolbar-tmpl').html();
			var tmpl = Handlebars.compile(src);
			$.extend(json['init'], {usr_logo: 'img/face.png', uni_name:$.cookie('zabeta_uni_name')});
			var html = tmpl(json);
			$('#toolbar').html(html);
		}else{
			initUniPicker();
		}
	});
}

function loadMenu(){
	var src = $('#menu-tmpl').html();
	var tmpl = Handlebars.compile(src);
	menuJson = {
			"items":
				[{
					"hash":	"tasks",
					"name":	"Tasks"
				},
				{
					"hash":	"form",
					"name":	"Form"
				},
				{
					"hash": "course",
					"name":	"Course"
				}]
	}
	$('#menu-content').html(tmpl(menuJson));
	if(window.location.hash.indexOf('course') != -1){
		loadCourseList();
	}
}

function loadCourseList(){
	$.get('api/Course/list', function(json){
		var src = $('#submenu-tmpl').html();
		var tmpl = Handlebars.compile(src);
		$('#course-sub').html(tmpl(json));
	});
}

function loadTasksList() {
  taskListJson = {
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
	var source = $("#list-tmpl").html();
	var template = Handlebars.compile(source);
	$('#content').html(template(taskListJson));
}

/* Temp proof-of-concept fn */
function loadForm(){
	formJson = { "fields" : [ { "name" : "description",
        "properties" : [ { "property" : "rows",
            "value" : "5"
          },
          { "property" : "cols",
            "value" : "10"
          }
        ],
      "textarea" : true,
      "type" : "textarea"
    },
    { "name" : "name",
      "type" : "text"
    },
    { "list" : true,
      "name" : "occupation",
      "options" : [ { "text" : "Scientist",
            "value" : "Scientist_id"
          },
          { "text" : "Engineer",
            "value" : "Engineer_id"
          },
          { "text" : "Philosopher",
            "value" : "Philosopher_id"
          }
        ],
      "properties" : [ { "property" : "class",
            "value" : "whatever"
          } ],
      "type" : "list"
    }
  ] };
	updateForm();
}

/* Temp proof-of-concept fn */
function addAnotherInput(){
	formJson.fields.push({
    	"type": "text",
    	"name": "another_input"
    	});
	updateForm();
}

/* Temp proof-of-concept fn */
function updateForm(){
	var source = $('#form-tmpl').html();
	var template = Handlebars.compile(source);
	$('#content').html(template(formJson));
}

function loadCourseData(course_id){
	$.getJSON('/api/mora/'+course_id, function(json){
		var source=$('#course-tmpl').html();
		var template = Handlebars.compile(source);
		$('#content').html(template(json));
	});
}
