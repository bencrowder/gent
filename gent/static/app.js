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
				url: '/ws/target/update-item-order/?order=' + order,
				method: 'POST',
				success: function(data) {
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
		},
	});
});
