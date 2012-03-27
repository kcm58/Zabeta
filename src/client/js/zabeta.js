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
			$.ajax('/api/crud/'+Zabeta.me.get('university'), {
				type: 'GET',
				async: false,
				success: function (response) {
					var uni_name = response['name'];
					var login_path = response['login_path'];
					Zabeta.me.set('uni_name', uni_name);

					// render the toolbar template
					T.render('toolbar', function (template) {
						$('#toolbar').html(template(Zabeta.me.toJSON()));
					});

					// TODO: program chooser, but again this data should be loaded
					// when all the initial data is loaded.
				}
			});
		},

		/** Called when the document has loaded its DOM and is ready. */
		applicationDidFinishLaunching: function () {
			// get the user
			$.ajax('/api/user/get', {
				type: 'GET',
				async: false,
				success: function (response) {
					if (!$.isEmptyObject(response.user)) {
						Zabeta.me = new Zabeta.User(response.user);
						Zabeta.displayToolbar();
					} else {
						// TODO: handle error
					}
				}
			});

			// switch to this users default page
			// TODO: check access level and load either the admin page or
			// the dashboard
			Zabeta.adminPage.show();
		}
	};
}();


/**
 * User
 */
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

Zabeta.UserList = Backbone.Collection.extend({
	model: Zabeta.User,

	url: function () {
		return 'api/crud/' + Zabeta.me.get('university') + '/users';
	}
});

Zabeta.UserListItemView = Backbone.View.extend({
	tagName: 'tr',

	render: function () {
		var self = this;
		T.render('user_list_item', function (template) {
			$(self.el).html(template(self.model.toJSON()));
		});
		return this;
	}
});

Zabeta.UserListView = Backbone.View.extend({
	el: $('#user-list tbody'),

	initialize: function () {
		this.model.bind('reset', this.render, this);
		var self = this;
		this.model.bind('add', function (user) {
			$(self.el).append(new Zabeta.UserListItemView({
				model:user
			}).render().el);
		});
	},

	render: function () {
		_.each(this.model.models, function (user) {
			$('#user-list tbody').append(new Zabeta.UserListItemView({
				model:user
			}).render().el);
		}, this);
		return this;
	}
});


/**
 * Program
 */
Zabeta.Program = Backbone.Model.extend({
	defaults: function () {
		return {
		};
	}
});

Zabeta.ProgramList = Backbone.Collection.extend({
	model: Zabeta.Program,

	url: function () {
		return 'api/crud/' + Zabeta.me.get('university') + '/programs';
	}
});

Zabeta.ProgramListView = Backbone.View.extend({
	el: $('#program-list tbody')
});

/**
 * Semester
 */
Zabeta.Semester = Backbone.Model.extend({
	defaults: function () {
		return {
		};
	}
});

Zabeta.SemesterList = Backbone.Collection.extend({
	model: Zabeta.Semester,

	url: function () {
		return 'api/crud/' + Zabeta.me.get('university') + '/semesters';
	}
});

Zabeta.SemesterListView = Backbone.View.extend({
	el: $('#semester-list tbody')
});

/**
 * Administrators page
 */
Zabeta.adminPage = function () {
	/* Privates */
	var layout = 'admin_layout';

	/* Public */
	return {
		programs: null,
		semesters: null,
		users: null,

		show: function () {
			Zabeta.switchLayout(layout);
			this.programs = new Zabeta.ProgramList;
			this.programs.fetch();

			this.semesters = new Zabeta.SemesterList;
			this.semesters.fetch();

			this.users = new Zabeta.UserList;
			this.userListView = new Zabeta.UserListView({model:this.users});
			this.users.fetch();
		}
	};
}();


$(document).ready(Zabeta.applicationDidFinishLaunching);
