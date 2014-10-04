$(document).ready(function() {
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
	$("#add-item").on("click", function(e) {
		// Clear out form
		$("form#add-modal textarea[name=title]").val('');
		$("form#add-modal input[name=family]").val('');
		$("form#add-modal textarea[name=notes]").val('');
		$("form#add-modal input[name=tags]").val('');

		$(".background").fadeIn(200);
		$("form#add-modal").slideDown(200);

		return false;
	});

	$("#add-modal").on("submit", function(e) {
		var url = "/ws/item/";

		var title = $("textarea[name=title]").val().trim();
		var family = $("input[name=family]").val().trim();
		var notes = $("textarea[name=notes]").val().trim();
		var tags = $("input[name=tags]").val().trim();

		if (title != '' && family != '') {
			$.ajax({
				url: url,
				method: "POST",
				data: {
					title: title,
					family: family,
					tags: tags,
					notes: notes,
				},
				success: function(data) {
					// Close modal
					$("form#delete-modal").slideUp(200);
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
	$("#edit-link").on("click", function(e) {
		// Fill in details
		var itemId = $("#item-header").attr("data-id");
		var title = $("#item-title").html();
		var family = $("a.family-link").attr("data-id");
		var notes = $("#notes-text").html();
		var tags = $("#item-tags").attr("data-tags");
		var dateCreated = $("#date-created").attr("data-date");
		var dateCompleted = $("#date-completed").attr("data-date");

		$("form#edit-modal textarea[name=title]").val(title);
		$("form#edit-modal input[name=family]").val(family);
		$("form#edit-modal textarea[name=notes]").val(notes);
		$("form#edit-modal input[name=tags]").val(tags);
		$("form#edit-modal input[name=datecreated]").val(dateCreated);
		$("form#edit-modal input[name=datecompleted]").val(dateCompleted);

		// Add item id to edit modal
		$("form#edit-modal").attr("data-item-id", itemId);

		$(".background").fadeIn(200);
		$("form#edit-modal").slideDown(200);

		return false;
	});

	$("#edit-modal").on("submit", function(e) {
		var url = "/ws/item/";

		var itemId = $("#item-header").attr("data-id");
		var title = $(this).find("textarea[name=title]").val().trim();
		var family = $(this).find("input[name=family]").val().trim();
		var notes = $(this).find("textarea[name=notes]").val().trim();
		var tags = $(this).find("input[name=tags]").val().trim();
		var dateCreated = $(this).find("input[name=datecreated]").val();
		var dateCompleted = $(this).find("input[name=datecompleted]").val();

		if (title != '') {
			url += "?item_id=" + itemId;

			$.ajax({
				url: url,
				method: "PUT",
				data: {
					family: family,
					title: title,
					tags: tags,
					notes: notes,
					datecreated: dateCreated,
					datecompleted: dateCompleted,
				},
				success: function(data) {
					console.log(data);
				
					// Close modal
					$("form#edit-modal").slideUp(200);
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
	$("#delete-link").on("click", function(e) {
		$(".background").fadeIn(200);
		$("form#delete-modal").slideDown(200);

		// Add item id to delete modal
		var itemId = $("#item-header").attr("data-id");
		$("form#delete-modal").attr("data-item-id", itemId);

		return false;
	});

	$("#delete-modal").on("submit", function(e) {
		var url = "/ws/item/";
		var itemId = $("#item-header").attr("data-id");
		var familyUrl = $("#item-header").attr("data-family-url");

		if (itemId != '') {
			url += "?item_id=" + itemId;

			$.ajax({
				url: url,
				method: "DELETE",
				success: function(data) {
					console.log(data);

					// Close modal
					$("form#delete-modal").slideUp(200);
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


	// Close modal
	$("form.modal a.cancel-link").on("click", function() {
		$(this).parent("form.modal").slideUp(200);
		$(".background").fadeOut(200);

		return false;
	});
});
