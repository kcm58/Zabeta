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
			"course/:course_id":	"course",
			"tasks": 				"loadTasks",
			"form":					"loadForm",
			"*data" : 				"default"
		},

		default: function(data){
			console.log("Hash passed data: "+data);
			loadDefault();
		},

		course: function(course_id){
			console.log("You want to load the course with ID "+course_id);
		},
		
		loadTasks: function(){
			loadTasksList();
		},
		
		loadForm: function(){
			loadForm();
		}
	});

	var router = new Router;
	Backbone.history.start();
}

function checkAuth(){
	$.get('/api/init/get', function(json){
		if($.isEmptyObject(json)){
			initUniPicker();
		}else{
			loadToolbar();
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
		$('#container').html(html);
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

function loadDefault(){
	$('#container').html('<a href="#tasks">Tasks</a><br /><a href="#form">Form</a>');
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
	$('#container').html(template(taskListJson));
}

/* Temp proof-of-concept fn */
function loadForm(){
	formJson = {
			"id": "test_form",
			"name": "test_form",
			"fields": [
			           {"label": "Name",
			        	"element": "input",
			        	"type": "text",
			        	"name": "name",
			        	"line_split": "<br /><br />",
			        	"label_line_break": "<br />"
			        	},
			        	{"label": "password",
			        	"element": "input",
			        	"type": "password",
			        	"name": "password",
			        	"line_split": "<br /><br />",
			        	"label_line_break": "<br />"
			        	},
			        	{"label": "Checkbox one",
			        	"element": "input",
			        	"type": "checkbox",
			        	"name": "cb1"
			        	},
			        	{"label": "Checkbox two",
			        	"element": "input",
			        	"type": "checkbox",
			        	"name": "cb2",
			        	"line_split": "<br /><br />"
			        	},
			        	{"label": "Yes",
			        	"element": "input",
			        	"type": "radio",
			        	"name": "yesno",
			        	"value": "1"
			        	},
			        	{"label": "No",
			        	"element": "input",
			        	"type": "radio",
			        	"name": "yesno",
			        	"value": "0",
			        	"line_split": "<br /><br />"
			        	},
			        	{"label": "Notes",
			        	"element": "textarea",
			        	"name": "notes",
			        	"label_line_break": "<br />",
			        	"closing_tag": "</textarea>",
			        	"line_split": "<br /><br />"
			        	},
			        	{"element": "input",
			        	"type": "button",
			        	"value": "Button!"
			        	}
			           ]};
	updateForm();
}

/* Temp proof-of-concept fn */
function addAnotherInput(){
	formJson.fields.push({"label": "Another Input",
    	"element": "input",
    	"type": "text",
    	"name": "another_input",
    	"line_split": "<br /><br />",
    	"label_line_break": "<br />"
    	});
	updateForm();
}

/* Temp proof-of-concept fn */
function updateForm(){
	var source = $('#form-tmpl').html();
	var template = Handlebars.compile(source);
	$('#container').html(template(formJson));
}
