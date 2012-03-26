/* ===================================================
 * js/zabeta.js
 * ========================================================== */

/*
 * Create a Zabeta namespace
 */
Zabeta = function () {
	/* Privates */
	// ...

	/* Public */
	return {
		adminLayout: 'admin_layout',
		dashboardLayout: 'dashboard_layout',
		collectionLayout: 'collection_layout',

		switchLayout: function (layout) {
			T.render(layout, function (template) {
				$('#container').html(template());
			});
		},

		/** holds the current users object */
		me: null,

		/** load the university data and display the toolbar */
		displayToolbar: function () {
			// TODO: the university should be loaded in conjunction with the
			// user and any other initial data (see similar note in
			// api/user.py).
			$.getJSON('/api/crud/'+Zabeta.me.get('university'), function (uni_json) {
				var uni_name = uni_json['name'];
				var login_path = uni_json['login_path'];
				Zabeta.me.set('uni_name', uni_name);

				// render the toolbar template
				T.render('toolbar', function (template) {
					console.dir(Zabeta.me.toJSON());
					console.dir(template(Zabeta.me.toJSON()));
					$('#toolbar').html(template(Zabeta.me.toJSON()));
				});

				// TODO: program chooser, but again this data should be loaded
				// when all the initial data is loaded.

			});
		},

		/** Called when the document has loaded its DOM and is ready. */
		applicationDidFinishLaunching: function () {
			console.log('Zabeta.applicationDidFinishLaunching');

			// get the user
			$.getJSON('/api/user/get', function (response) {
				if (!$.isEmptyObject(response.user)) {
					Zabeta.me = new Zabeta.User(response.user);
					Zabeta.displayToolbar();
				} else {
					// TODO: handle error
				}
			});

			// switch to this users default layout
			// TODO: check access level and load either the admin page or
			// the dashboard
			Zabeta.switchLayout(Zabeta.adminLayout);
		}
	};
}();


Zabeta.User = Backbone.Model.extend({
	defaults: function () {
		return {
			full_name: '',
			display_name: '',
			email: '',
			employee_id: '',
			phone_office: '',
			phone_personal: '',
			office: '',
			join_date: '',
			depart_date: '',
			thumbnail: '',
			webpage: '',
			tasks: null,
			usr_logo: 'img/face.png'
		};
	}
});

Zabeta.Users = Backbone.Collectioin.extend({
	model: Zabeta.User
});


Zabeta.Program =  Backbone.Model.extend({
	defaults: function () {
		return {
		};
	}
});

Zabeta.Programs = Backbone.Collectioin.extend({
	model: Zabeta.Program
});


Zabeta.Semester =  Backbone.Model.extend({
	defaults: function () {
		return {
		};
	}
});

Zabeta.Semesters = Backbone.Collectioin.extend({
	model: Zabeta.Semester
});


Zabeta.adminPage = function () {
	/* Privates */
	// ...

	/* Public */
	return {

	};
}();


$(document).ready(Zabeta.applicationDidFinishLaunching);
