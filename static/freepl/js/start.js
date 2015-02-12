$(document).ready(function() {
	$('a.login-window').click(function() {
		$('#signup').hide();
		// Getting the variable's value from a link 
		var loginBox = $(this).attr('href');
		console.log("hello")
		console.log($(loginBox))
		//Fade in the Popup and add close button
		$(loginBox).fadeIn(300);
		
		//Set the center alignment padding + border
		var popMargTop = ($(loginBox).height() + 100) / 2; 
		var popMargLeft = ($(loginBox).width() + 24) / 2; 
		console.log(popMargTop);
		console.log(popMargLeft);
		$(loginBox).css({ 
			'margin-top' : -popMargTop,
			'margin-left' : -popMargLeft,
		});
		
		// Add the mask to body
		$('body').append('<div id="mask"></div>');
		$('#mask').fadeIn(300);
		
		return false;
	});
	
	
	// When clicking on the button close or the mask layer the popup closed
	$('a.close, #mask').live('click', function() { 
	  $('#mask , .login-popup').fadeOut(300 , function() {
		$('#signin').show();
		$('#mask').remove();  
	}); 
	return false;
	});


	//  player selection close button
	var plcount=0;
	var locked=0;

	$('.item').hide();
	
	$('.cross').click(function(){
		var par=$(this).parent();
		var inst=($(this).parent()).parent();
		var idinst=inst.attr("id");
		
		inst.fadeOut();
		par.children(".dp").remove();
		par.children(".tempName").remove();
		par.children(".tempPrice").remove();
		inst.attr({'class':"item"});
		$("#"+idinst).fadeIn();
		if(plcount>0)
		{
			plcount--;
		}
		



	});
	

	$('.rc1').click(function(){
		if(plcount<11 && locked!=1)
		{
			
			$(this).fadeOut();
			var temp=$(this).children(".temp").html();
			
			var plid=$(this).attr("id");
			$('.item').eq(plcount).fadeIn();
			$('.item').eq(plcount).addClass(plid);
			$("."+plid+" div").append(temp);
			temp=null;
			plcount++;
			alert(plcount);
			

		}
		
		

	})
	
});
