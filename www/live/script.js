var g;
var session = [];
$(document).ready(function() {
    
    var w1 = $(window).width();
    var h1 = $(window).height();
    
    var w2 = $('#readings').width();
    
    $('#graph').width(w1-w2-100);
    $('#graph').height(h1-100);
    
    var live = false;
    setInterval(function() {
	$.ajax('latest.json', {
	    cache: false,
	    ifModified: true,
	    dataType: 'json',
	    timeout: 500,
	    success: function(data) {
		
		if(!data) return;
		
		if(data['pulse'] == 0 && data['target_pulse'] == 0 && data['power'] == 0 && data['rpm'] == 0) return;
		
		if(!live) {
		    live = true;
		    $('.standby').hide().removeClass('blink');
		    $('.live').show().addClass('blink');
		    $('timestamp').show();
		 
		    session += data['timestamp'] + ',' + data['pulse'] + ',' + data['target_pulse'] + ',' + data['power'] + ',' + data['rpm'] + '\n';
		    //session += (new Date(data['timestamp'])).getTime() + ',' + data['pulse'] + ',' + data['target_pulse'] + ',' + data['power'] + ',' + data['rpm'] + '\n';
		    g = new Dygraph($('#graph').get(0), session, {
			labels: ['Time', 'Pulse', 'Target pulse', 'Power', 'Rpm'],
			colors: ['#dd0000', '#0000dd', '#00dd00', '#dddd00'],
			//valueRange: [0, 200],
			displayAnnotations: true,
			labelsSeparateLines: true,
			hideOverlayOnMouseOut: false,
			legend: 'always'
		    });
		}
		console.log(data);
		_.each(['timestamp', 'pulse', 'target_pulse', 'power', 'rpm'], function(stat) {
		    $('.' + stat).text(data[stat]);
		});
		
		console.log(session);
		
		session += data['timestamp'] + ',' + data['pulse'] + ',' + data['target_pulse'] + ',' + data['power'] + ',' + data['rpm'] + '\n';
		//session += (new Date(data['timestamp'])).getTime() + ',' + data['pulse'] + ',' + data['target_pulse'] + ',' + data['power'] + ',' + data['rpm'] + '\n';
		g.updateOptions({ 'file': session });
	    }
	});
    }, 1000);
    
    setInterval(function() {
	$('.blink').addClass('shadow');
	$('.blink').fadeTo(0, 1.00, function() {
	    $(this).fadeTo(500, 0.85, function() {
		$('.blink').removeClass('shadow');
	    });
	});
    }, 1500);
});
