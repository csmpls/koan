
$('#removebutton').click(function() {
	
	var post = 	$('.post').attr('id')

	ajaxy('/delete',post)

})

$('.submit').click(function() {

		var submission = $('#koan_submission').val()

		ajaxy('/post',submission)

})

function ajaxy(route,item) {

	$.ajax({
			type: "POST",
			url: route,
			contentType: 'application/json',
			 	dataType:'json',
			data: JSON.stringify({payload:item}),
			success: function(data) {


				if (route === '/post') {

					// empty submission field
					$('#koan_submission').val('')
				}

				// post newest submission to page
				$('.post').html(data.post)
				$('.post').attr('id',data.id)
			}
		})
}


