$(document).ready(function() {
	// From https://gist.github.com/alanhamlett/6316427
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE' || settings.type == 'PATCH') {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});


	$("ul.sortable").sortable({
		placeholder: "placeholder container",
		update: function(event, ui) {
			var order = [];
			var items = ui.item.parents("ul:first").find("li");

			for (var i=0; i<items.length; i++) {
				var item = $(items[i]);
				order.push(item.attr("data-id"));
			}

			$.ajax({
				url: '/ws/family/update-item-order/?order=' + order,
				method: 'POST',
				success: function(data) {
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
		},
	});


	$("#item-header").on("touchstart click", function() {
		var item_id = $(this).attr("data-id");
		var item = $(this);

		// Toggle completion
		$.ajax({
			url: '/ws/item/toggle-complete/?item_id=' + item_id,
			method: 'POST',
			success: function(data) {
				item.toggleClass("completed");
				return false;
			},
			error: function(data) {
				console.log("Error! :(", data);
				return false;
			},
		});

		return false;
	});


	// Add item
	$("#add-item").on("click", showAddItemModal);

	Mousetrap.bind('ctrl+enter', showAddItemModal);

	function showAddItemModal() {
		// Clear out form
		$("form#add-modal textarea[name=title]").val('');
		$("form#add-modal input[name=family]").val('');
		$("form#add-modal textarea[name=notes]").val('');
		$("form#add-modal input[name=tags]").val('');

		$(".background").fadeIn(200);
		$("form#add-modal").slideDown(200);
		$("form#add-modal textarea[name=title]").focus();

		window.scrollTo(0, 0);

		return false;
	}

	// Shift+return to add/save
	Mousetrap.bindGlobal('shift+return', function(e) {
		// Add item
		if ($("form#add-modal:visible").length) {
			// Submit add modal
			$("form#add-modal").submit();
			return false;
		}

		// Edit item
		if ($("form#edit-item-modal:visible").length) {
			// Submit item edit modal
			$("form#edit-item-modal").submit();
			return false;
		}

		// Edit family
		if ($("form#edit-family-modal:visible").length) {
			// Submit family edit modal
			$("form#edit-family-modal").submit();
			return false;
		}
	});

	$("#add-modal").on("submit", function(e) {
		var url = "/ws/item/";

		var title = $("textarea[name=title]").val().trim();
		var family = $("input[name=family]").val().trim();
		var familyBox = $("input[name=family-box]").val().trim();
		var notes = $("textarea[name=notes]").val().trim();
		var tags = $("input[name=tags]").val().trim();

		if (title != '' && (family != '' || familyBox != '')) {
			$.ajax({
				url: url,
				method: "POST",
				data: {
					title: title,
					family: family,
					family_box: familyBox,
					tags: tags,
					notes: notes,
				},
				success: function(data) {
					// Close modal
					$("form#add-modal").slideUp(200);
					$(".background").fadeOut(200);

					// Redirect to new item page
					window.location.href = "/item/" + data.id;
				},
				error: function(data) {
					console.log("Error! :(");
					console.log(data);
				},
			}, 'json');
		}

		return false;
	});


	// Edit item
	$("#edit-item-link").on("click", function(e) {
		$(".background").fadeIn(200);
		$("form#edit-item-modal").slideDown(200);
		$("form#edit-item-modal textarea[name=title]").focus();

		window.scrollTo(0, 0);

		return false;
	});

	$("#edit-item-modal").on("submit", function(e) {
		var url = "/ws/item/";

		var itemId = $("#item-header").attr("data-id");
		var title = $(this).find("textarea[name=title]").val().trim();
		var family = $(this).find("input[name=family]").val().trim();
		var familyBox = $("input[name=family-box]").val().trim();
		var notes = $(this).find("textarea[name=notes]").val().trim();
		var tags = $(this).find("input[name=tags]").val().trim();
		var dateCreated = $(this).find("input[name=datecreated]").val();
		var dateCompleted = $(this).find("input[name=datecompleted]").val();
		var starred = $(this).find("input[name=starred]").val();
		console.log(starred);

		if (title != '') {
			url += "?item_id=" + itemId;

			$.ajax({
				url: url,
				method: "PUT",
				data: {
					family: family,
					family_box: familyBox,
					title: title,
					tags: tags,
					notes: notes,
					datecreated: dateCreated,
					datecompleted: dateCompleted,
					starred: starred,
				},
				success: function(data) {
					// Close modal
					$("form#edit-item-modal").slideUp(200);
					$(".background").fadeOut(200);

					// Redirect to new item page
					window.location.href = "/item/" + itemId;
				},
				error: function(data) {
					console.log("Error! :(");
					console.log(data);
				},
			}, 'json');
		}

		return false;
	});


	// Delete item
	$("#delete-item-link").on("click", function(e) {
		$(".background").fadeIn(200);
		$("form#delete-item-modal").slideDown(200);

		return false;
	});

	$("#delete-item-modal").on("submit", function(e) {
		var url = "/ws/item/";
		var itemId = $("#item-header").attr("data-id");
		var familyUrl = $("#item-header").attr("data-family-url");

		if (itemId != '') {
			url += "?item_id=" + itemId;

			$.ajax({
				url: url,
				method: "DELETE",
				success: function(data) {
					// Close modal
					$("form#delete-item-modal").slideUp(200);
					$(".background").fadeOut(200);

					// Redirect to family page
					window.location.href = familyUrl;
				},
				error: function(data) {
					console.log("Error! :(");
					console.log(data);
				},
			}, 'json');
		}

		return false;
	});


	// Edit family
	$("#edit-family-link").on("click", function(e) {
		$(".background").fadeIn(200);
		$("form#edit-family-modal").slideDown(200);
		$("form#edit-family-modal #edit-husband-name").focus();

		return false;
	});

	$("#edit-family-modal").on("submit", function(e) {
		var url = "/ws/family/";

		var familyId = $("#family-header").attr("data-id");
		var husbandName = $(this).find("input[name=husband-name]").val().trim();
		var husbandId = $(this).find("input[name=husband-id]").val().trim();
		var wifeName = $(this).find("input[name=wife-name]").val().trim();
		var wifeId = $(this).find("input[name=wife-id]").val().trim();
		var notes = $(this).find("textarea[name=notes]").val().trim();
		var tags = $(this).find("input[name=tags]").val().trim();
		var dateCreated = $(this).find("input[name=datecreated]").val();
		var starred = $(this).find("input[name=starred]").val();

		if (husbandName != '' || wifeName != '') {
			url += "?family_id=" + familyId;

			$.ajax({
				url: url,
				method: "PUT",
				data: {
					husband_name: husbandName,
					husband_id: husbandId,
					wife_name: wifeName,
					wife_id: wifeId,
					tags: tags,
					notes: notes,
					datecreated: dateCreated,
					starred: starred,
				},
				success: function(data) {
					// Close modal
					$("form#edit-family-modal").slideUp(200);
					$(".background").fadeOut(200);

					// Reload the page
					window.location.href = "/family/" + familyId;
				},
				error: function(data) {
					console.log("Error! :(");
					console.log(data);
				},
			}, 'json');
		}

		return false;
	});


	// Delete family
	$("#delete-family-link").on("click", function(e) {
		$(".background").fadeIn(200);
		$("form#delete-family-modal").slideDown(200);

		return false;
	});

	$("#delete-family-modal").on("submit", function(e) {
		var url = "/ws/family/";
		var familyId = $("#family-header").attr("data-id");

		if (familyId != '') {
			url += "?family_id=" + familyId;

			$.ajax({
				url: url,
				method: "DELETE",
				success: function(data) {
					// Close modal
					$("form#delete-family-modal").slideUp(200);
					$(".background").fadeOut(200);

					// Redirect to home page
					window.location.href = "/";
				},
				error: function(data) {
					console.log("Error! :(");
					console.log(data);
				},
			}, 'json');
		}

		return false;
	});


	// Close modal
	$("form.modal a.cancel-link").on("click", function() {
		$(this).parent("form.modal").slideUp(200);
		$(".background").fadeOut(200);

		return false;
	});

	$("form.modal").on("keyup", function(e) {
		if (e.keyCode == 27) {
			$(this).slideUp(200);
			$(".background").fadeOut(200);

			return false;
		}
	});


	// Autocomplete for family
	var options = {
		serviceUrl: '/ws/family/search/',
		formatResult: function(suggestion, currentValue) {
			var html = '<div id="' + suggestion.data.id + '"><label>' + suggestion.value.replace('/', '<span>/</span>') + '</label>';
			if (suggestion.data.subtitle) {
				html += '<span class="desc">' + suggestion.data.subtitle + '</span>';
			}
			html += '</div>';
			return html;
		},
		onSelect: function(suggestion) {
			familyBox = $(".family-box");

			// Hide input
			familyBox.hide();

			// Clear it out
			familyBox.val('');

			// Update the value
			familyBox.siblings("input[name=family]").val(suggestion.data.id);

			// Update the family display box
			familyBox.siblings("div.family-display").find("div").html(suggestion.value.replace('/', '<span>/</span>'));

			// Show the family display box
			familyBox.siblings("div.family-display").show();

			return false;
		},
		triggerSelectOnValidInput: false,
	};

	$(".family-box").autocomplete(options);


	// Family display
	$(".family-display a.delete").on("click", function() {
		var displayBox = $(this).parents(".family-display");

		// Clear out the value (because the user wants to type a new family in)
		displayBox.siblings("input[name=family]").val();

		// Hide the display box
		displayBox.hide();

		// Show the input and focus on it
		displayBox.siblings("input[name=family-box]").show().focus();

		return false;
	});	


	// General shortcuts
	Mousetrap.bind('h', function() {
		window.location.href = '/';
		return false;
	});

	Mousetrap.bind('/', function() {
		$("input#q").focus();
		return false;
	});


	// Tags
	$("input[name=tags]").tagit();


	// Autosize
	$("textarea[name=notes]").autosize();
	$("form.modal textarea[name=title]").autosize();


	// Starring items/families
	$("h2 .star").on("click", function() {
		var starredData = $(this).parents("h2:first").siblings("input[name=starred]");

		if ($(this).hasClass("starred")) {
			starredData.val(false);
			$(this).removeClass("starred");
		} else {
			starredData.val(true);
			$(this).addClass("starred");
		}

		return false;
	});
});


// From https://gist.github.com/alanhamlett/6316427
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i=0; i<cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
