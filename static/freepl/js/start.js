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
	/*$('a.close, #mask').live('click', function() { 
	  $('#mask , .login-popup').fadeOut(300 , function() {
		$('#signin').show();
		$('#mask').remove();  
	}); 
	return false; 
	});*/


	//  player selection close button

	var fix=null;
	var pcheck=null;
	var idfix=null;
	$('.fixture').click(function(){
		fix=$(this).attr("id");
		idfix=fix.substring(4);
		
		plcount=$(this).attr("data-plc");
		pcheck=$("#"+fix).attr("data-pcheck");
	});
	var plcount=0;
	var mod=0;
	var locked=0;
	for(var i=1;i<=15;i++)
	{
		$(".itemf"+i).hide();
	}
	
	/*
	$('.cross').click(function(){
		if (plcount>0) {
			plcount--;
		};
		$("#"+fix).attr({"data-plc":plcount});
		var par=$(this).parent(); // div
		var inst=($(this).parent()).parent(); // li item
		var ggpapa=inst.parent();
		var idinst=inst.attr("data-plid");
		par.removeClass("paparent");
		par.children(".power").removeClass("powactive");
		ggpapa.attr({'data-pstatus':0});
		par.children('.power').attr({'data-pow':0});

		

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
			$(".spnotice").delay(900).fadeIn();
		};
		



	});
	

	$('.rc1').click(function(){
		var fixid=$(this).attr("data-check");
		$("#spnotice"+fixid).hide();
		if(plcount<11 && locked!=1)
		{
			plcount++;
			$("#"+fix).attr({"data-plc":plcount});
			$(this).fadeOut(100);
			$(this).addClass("effect1");
			
			var temp=$(this).children(".temp").html();
			
			var plid=$(this).attr("id");
			
			$(".item"+fixid).eq(mod).fadeIn();
			$(".item"+fixid).eq(mod).css("display","inline-block");
			$(".item"+fixid).eq(mod).attr({'data-plid':plid});
			$(".item"+fixid).eq(mod).addClass(plid);
			$("."+plid+" div").append(temp);
			temp=null;
			mod++;
			
			
			

		}
		
		

	});
*/

// Second attempt

$('.rc1').click(function(){
		var fixid=$(this).attr("data-check");
		$("#spnotice"+fixid).hide();
		if(plcount<11 && locked!=1)
		{
			plcount++;
			$("#"+fix).attr({"data-plc":plcount});
			$(this).fadeOut(100);
			$(this).addClass("effect1");
			
			var temp=$(this).children(".temp").html();
			
			var plid=$(this).attr("id");
			
			$(".emp"+fixid).first().fadeIn();
			$(".emp"+fixid).first().css("display","inline-block");
			$(".emp"+fixid).first().attr({'data-plid':plid});
			$(".emp"+fixid).first().addClass(plid);
			var t=$(".emp"+fixid).first();
			t.removeClass("emp"+fixid);
			$("."+plid+" div").append(temp);
			temp=null;
			//mod++;
			
			
			

		}
		
		

	});

	$('.cross').click(function(){
		if (plcount>0) {
			plcount--;
		};
		$("#"+fix).attr({"data-plc":plcount});
		var par=$(this).parent(); // div
		var inst=($(this).parent()).parent(); // li item
		var ggpapa=inst.parent();
		var idinst=inst.attr("data-plid");
		par.removeClass("paparent");
		par.children(".power").removeClass("powactive");
		ggpapa.attr({'data-pstatus':0});
		par.children('.power').attr({'data-pow':0});

		

		par.children(".dp").remove();
		par.children(".tempName").remove();
		par.children(".tempPrice").remove();
		var cont1=inst.html();
		$('.teamgrid').append("<li class='item' style='display:none;'>"+cont1+"</li>");

		inst.fadeOut();
		//inst.addClass();
		inst.attr({'class':"emp"+idfix+" item"+idfix});
		$("#"+idinst).removeClass("effect1");
		$("#"+idinst).fadeIn();
		if (plcount==0) {
			$(".spnotice").delay(900).fadeIn();
		};
		



	});


$('.teamgrid').attr({'data-pstatus':0});
$('.power').attr({'data-pow':0});

	$('.power').click(function(){
		
		var current=$(this);

		var powstate=$(this).attr('data-pow');
		var currentpar=$(this).parent();
		var gpapapow=($(this).parent()).parent(); // li
		var gpapacl=gpapapow.attr("class"); 
		gpapacl=gpapacl.substring(4);
		gpapacl=gpapacl.substring(0,2);
		var ggpapapow=gpapapow.parent(); // teamgrid
		
		// cases

		// case 1: init
		var state=ggpapapow.attr('data-pstatus');
		
		
		//alert(state);
		//alert(powstate);
		if(state==0 && powstate==0) // No power player set
		{
			current.addClass("powactive");
			currentpar.addClass("paparent");
			current.attr({'data-pow':1});
			ggpapapow.attr({'data-pstatus':1});
		}
		else if (state==1 && powstate==1) // selected player is power player
		{
			current.removeClass("powactive");
			currentpar.removeClass("paparent");
			current.attr({'data-pow':0});
			ggpapapow.attr({'data-pstatus':0});
		};
	})

	// power play assignment
//	var pcheck=$("#"+fix).attr("data-pcheck");

	/* Power Play 
		
	$('.power').click(function(){
		var pow=$(this);

		var powparent=pow.parent();
		if(pcheck==0){
		$("#"+fix).attr({"data-pcheck":1});
		pow.addClass("powactive");
		powparent.addClass("paparent");
			pcheck=1;
			
		}
		else
		{
			$("#"+fix).attr({"data-pcheck":0});
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
		}); */
		

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
