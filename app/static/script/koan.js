
$('.submit').click(function() {

		var submission = $('#koan_submission').val()

		$.ajax({
			type: "POST",
			url: '/post',
			contentType: 'application/json',
			 	dataType:'json',
			data: JSON.stringify({submission:submission}),
			success: function(data) {

				// empty submission field
				$('#koan_submission').val('')
				
				// post newest submission to page
				$('#post').html(data.post)
			}
		})
	})


