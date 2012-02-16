/*
 * main.js
 */

$(document).ready(function(){
	loadBackbone();
	//initUniPicker();
});

function loadBackbone(){
	var Zabeta = Backbone.Controller.extend({
		api_url: "/api/",
		
		routes: {
		"*universityChooser":
		},
		
		defaultAction: function(universityChooser){
			if(universityChooser){
				var universityLoaderUrl = this.api_url+'University/list'
				
				this.loadData(universityLoaderUrl);
			}
		},
		loadData: function(pageUrl){
			
		}
	});
	
	
}

/*function initUniPicker(){
	
	var UniPicker = Backbone.View.extend({
		el: $('#main'),
		
		initialize: function(){
			//getJSON
			var json = {"universities":[{"uni_id":"1", "uni_name":"NAU"},{"uni_id":"2", "uni_name":"ASU"}]};
			_.bindAll(this, 'render');
			this.render(json);
		},
		
		render: function(json){
			loadUniPicker(json);
		}
	});
	
	var uniPicker = new UniPicker();
	 
}

function loadUniPicker(json){
	//alert(json);
	var src = $('#uni-template').html();
	var tmpl = Handlebars.compile(src);
	var html = tmpl(json);
	$('#main').html(html);
	
}*/