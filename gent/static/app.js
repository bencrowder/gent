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
});
