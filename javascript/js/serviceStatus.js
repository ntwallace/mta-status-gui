$(document).ready(function() {
	let rowCount = 0;
	let timestamp;

	// Pull XML from MTA file
	$.ajax({
	    url: 'serviceStatus.txt',
	    type: 'POST',
	    dataType: 'xml',
	    success: function(xml) {
	    	timestamp = $(xml).find('timestamp').text().replace(/:(\d{1,3})\s/g,'');
	        $(xml).find('subway').find('line').each(function(index){
	            let name = $(this).find('name').text();
	            let status = $(this).find('status').text();
	            let text = $(this).find('text').text();
	            let date = $(this).find('Date').text();
	            let time = $(this).find('Time').text();
	            if (time != '') {
	            	time = time;
	            } else {
	            	time = timestamp.substr(timestamp.indexOf(' '),timestamp.length);
	            }

	            // Write img tag, train status, and timestamp into train row DIVs || write delay text into hidden DIVs
	            $('.train').slice(rowCount, rowCount + 1).append('<div class=\'col\' id=\'img\'><img src=\'img/' + name + '.svg\' class=\'img-fluid\'></div><div class=\'col status\' id=' + name + '-status>' + status + '</div><div class=\'col text\' id=\'timestamp\'>' + time + '</div><br />');
	        	$('.details').slice(rowCount, rowCount + 1).append('<div class=\'col\'>' + text + '</div>');
	        	rowCount += 1;

	        });

	        $('.update').append('Updated ' + timestamp);

	        // Color status DIVs based on MTA status text
			$('.status').each(function(){
				if ($(this).text() === 'DELAYS') {
					$(this).css('background-color', 'red');
				} else if ($(this).text() === 'PLANNED WORK' || $(this).text() === 'SERVICE CHANGE') {
					$(this).css('background-color', 'yellow');
				} else {
					$(this).css('background-color', 'green');
				}
			});

	    },
	    error: function() {
	        $('.p').append("Failed to get xml");
	    }
	});

	// Show/hide hidden DIVs with delay text
	$('.train').click(function(){
		let id = $(this).attr('id');
		let detailId = '#' + id + '-details';
		let detailIdChild = detailId + ' > div.col'

		if ($(detailIdChild).text() != '') {
			$(detailId).slideToggle('slow');		
		}

	});

});
