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
	var mod=0;
	var locked=0;

	$('.item').hide();
	
	$('.cross').click(function(){
		if (plcount>0) {
			plcount--;
		};

		var par=$(this).parent(); // div
		var inst=($(this).parent()).parent(); // li item
		var idinst=inst.attr("data-plid");
		par.removeClass("paparent");
		par.children(".power").removeClass("powactive");

		


		par.children(".dp").remove();
		par.children(".tempName").remove();
		par.children(".tempPrice").remove();
		var cont1=inst.html();
		$('.teamgrid').append("<li class='item' style='display:none;'>"+cont1+"</li>");

		inst.fadeOut();
		
		inst.attr({'class':"item"});
		$("#"+idinst).removeClass("effect1");
		$("#"+idinst).fadeIn();
		if (plcount==0) {
			$('#spnotice').delay(900).fadeIn();
		};
		



	});
	

	$('.rc1').click(function(){
		$('#spnotice').hide();
		if(plcount<11 && locked!=1)
		{
			$(this).fadeOut(100);
			$(this).addClass("effect1");
			
			var temp=$(this).children(".temp").html();
			
			var plid=$(this).attr("id");
			
			$('.item').eq(mod).fadeIn();
			$('.item').eq(mod).css("display","inline-block");
			$('.item').eq(mod).attr({'data-plid':plid});
			$('.item').eq(mod).addClass(plid);
			$("."+plid+" div").append(temp);
			temp=null;
			mod++;
			plcount++;
			
			

		}
		
		

	});


	// power play assignment

	var pcheck=0;

	
		
	$('.power').click(function(){
		var pow=$(this);
		var powparent=pow.parent();
		if(pcheck==0){
		pow.addClass("powactive");
		powparent.addClass("paparent");
			pcheck=1;
			
		}
		else
		{
			pow.removeClass("powactive");
		powparent.removeClass("paparent");
			pcheck=0;
		}

	});
	
		$('.power').mouseover(function(){
			if(pcheck==0)
	{
			$(this).css("color","#3498DB");
		}
		});
		$('.power').mouseout(function(){
			if(pcheck==0)
	{
			$(this).css("color","#777");
		}
		});
		

	/*var pow=0;
	$('.item div').click(function(){
		if (pow==0) {
			$(this).addClass("powered");
			pow=1;
		};


	});
	$('.powered').click(function(){
		$(this).removeClass("powered");
		pow=0;


	}) */
	
});
