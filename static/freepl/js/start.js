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

	var selectedpl=[];
	function storepl()
	{
		for (var i = 0; i <11; i++) {
			var tempor=$(".item"+newfix).eq(i).attr("data-plid");
			var powcheck=$(".item"+newfix).eq(i).children().attr("class");
			if(powcheck=="paparent")
			{
				tempor="*"+tempor;
			}
			selectedpl.push(tempor);
			alert(selectedpl);
		}
	}
	
	//initialized values for roles
	var rbowl=0;
	var rbat=0;
	var rall=0;
	var rwk=0;
	
	function plych(rbowl,rbat,rwk,rall,fix)
	{
		if (rbat>=4) {
			$(".bat"+fix).removeClass("ntd");
			$(".bat"+fix).addClass("done");

		};
		if (rbat<4) {
			$(".bat"+fix).addClass("ntd");
			$(".bat"+fix).removeClass("done");

		};


		if (rbowl>=2) {
			$(".bowl"+fix).removeClass("ntd");
			$(".bowl"+fix).addClass("done");

		};
		if (rbowl<2) {
			$(".bowl"+fix).addClass("ntd");
			$(".bowl"+fix).removeClass("done");

		};


		if (rwk==1) {
			$(".wk"+fix).removeClass("ntd");
			$(".wk"+fix).addClass("done");

		};
		if (rwk!=1) {
			$(".wk"+fix).addClass("ntd");
			$(".wk"+fix).removeClass("done");

		};
		


		if (rall>=2) {
			$(".all"+fix).removeClass("ntd");
			$(".all"+fix).addClass("done");

		};
		if (rall<2) {
			$(".all"+fix).addClass("ntd");
			$(".all"+fix).removeClass("done");

		};


	}

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
	var newfix=null;
	var pcheck=null;
	var idfix=null;
	var budget=1000;

	var counA=null;
	var counB=null;
	var numA=0;
	var numB=0;
	$('.fixture').click(function(){

		counA=$(this).attr("data-countryA");
		counB=$(this).attr("data-countryB");
		numA=$(this).attr("data-numA");
		numB=$(this).attr("data-numB");
		Tspread=0;
		//alert(counA+" ,"+counB);
		fix=$(this).attr("id");
		newfix=fix.substring(4);
		idfix=fix.substring(4);
		budget=parseInt($(".bud"+newfix).html());
		//alert(budget);
		plcount=$(this).attr("data-plc");
		pcheck=$("#"+fix).attr("data-pcheck");



		rbowl=0;rbat=0;rwk=0;rall=0;
		for (var i = 0; i <11; i++) {
				temprole=$(".temp"+fix).eq(i).attr("data-role");

				if(temprole=="rolebowl")
				{
					rbowl++;
					temprole=null;
				}
				if(temprole=="rolebat")
				{
					rbat++;
					temprole=null;
				}
				if(temprole=="roleallround")
				{
					rall++;
					temprole=null;
				}
				if(temprole=="rolewk")
				{
					rwk++;
					temprole=null;
				}
			};
			var fncall=plych(rbowl,rbat,rwk,rall,fix);

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

var currpow=0;
var temprole=null;
var price=0;
var Tspread=0;
$('.rc1').click(function(){
		var fixid=$(this).attr("data-check");
		var thispl=$(this);
		$("#spnotice"+fixid).hide();
		if(plcount<11 && locked!=1)
		{
			plcount++;
			
			$("#"+fix).attr({"data-plc":plcount});
			$(this).fadeOut(100);
			$(this).addClass("effect1");

			// Team SPread Count
			var tempcoun=($(this).children(".temp")).children(".tempName").attr("data-country");
			//alert(tempcoun);
			if(tempcoun==counA)
			{
				numA++;
				$("#"+fix).attr({'data-numA':numA});
			}
			if (tempcoun==counB) {
				numB++;
				$("#"+fix).attr({'data-numB':numB});
			};
			Tspread=Math.max(numA,numB);
			if (Tspread>6) {
				$(".spr"+newfix).removeClass("done");
				$(".spr"+newfix).addClass("ntd");
			};
			if (Tspread<=6) {
				$(".spr"+newfix).removeClass("ntd");
				$(".spr"+newfix).addClass("done");
			};
			var spr=Tspread.toString();
			//alert(spr);

			$(".sprval"+newfix).html(spr);


			var temp=$(this).children(".temp").html();
			
			var plid=$(this).attr("id");
			//Budget changes
			price=parseInt((thispl.children(".temp")).children(".tempPrice").attr("data-price"));
			budget=budget-price;
			if (budget<0) {
				$(".bud"+newfix).addClass("lowbudget");
			};
			if (budget>0) {
				$(".bud"+newfix).removeClass("lowbudget");
			};
			var stbud=budget.toString();
			//alert(stbud);
			$(".bud"+newfix).html(stbud);
			var role=thispl.children(".role").attr("data-role");
			var scancl="item"+thispl.attr("data-check");
			
			

			$(".emp"+fixid).first().fadeIn();
			$(".emp"+fixid).first().css("display","inline-block");
			$(".emp"+fixid).first().attr({'data-plid':plid});
			$(".emp"+fixid).first().addClass(plid);
			$(".emp"+fixid).first().attr({'data-role':role});
			
			var scanpar=$("."+scancl).parent();
			for (var i = 0; i <11; i++) {
				temprole=scanpar.children("."+scancl).eq(i).attr("data-role");

				if(temprole=="rolebowl")
				{
					rbowl++;
					temprole=null;
				}
				if(temprole=="rolebat")
				{
					rbat++;
					temprole=null;
				}
				if(temprole=="roleallround")
				{
					rall++;
					temprole=null;
				}
				if(temprole=="rolewk")
				{
					rwk++;
					temprole=null;
				}
			};
			
			
			var fncall=plych(rbowl,rbat,rwk,rall,fixid);
			rbat=0;rwk=0;rbowl=0;rall=0;



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


		// Team SPread Count
			var tempcount=par.children(".tempName").attr("data-country");
			//alert(tempcoun);
			if(tempcount==counA)
			{
				numA--;
				$("#"+fix).attr({'data-numA':numA});
			}
			if (tempcount==counB) {
				numB--;
				$("#"+fix).attr({'data-numB':numB});
			};
			Tspread=Math.max(numA,numB);
			if (Tspread>6) {
				$(".spr"+newfix).removeClass("done");
				$(".spr"+newfix).addClass("ntd");
			};
			if (Tspread<=6) {
				$(".spr"+newfix).removeClass("ntd");
				$(".spr"+newfix).addClass("done");
			};
			var spr=Tspread.toString();
			//alert(spr);

			$(".sprval"+newfix).html(spr);


		if(par.children('.power').attr("data-pow")==1)
		{
			par.removeClass("paparent");
			par.children(".power").removeClass("powactive");
			ggpapa.attr({'data-pstatus':0});
			par.children('.power').attr({'data-pow':0});
			$(".pow"+newfix).addClass("ntd");
			$(".pow"+newfix).removeClass("done");
		}
		price=parseInt(par.children(".tempPrice").attr("data-price"));
		
			budget=budget+price;
			if (budget<0) {
				$(".bud"+newfix).addClass("lowbudget");
			};
			if (budget>0) {
				$(".bud"+newfix).removeClass("lowbudget");
			};
			var stbudd=budget.toString();
			//alert(stbud);
			$(".bud"+newfix).html(stbudd);

		par.children(".dp").remove();
		par.children(".tempName").remove();
		par.children(".tempPrice").remove();
		par.children(".rl").remove();
		par.children(".coun").remove();



		var cont1=inst.html();
		$('.teamgrid').append("<li class='item' style='display:none;'>"+cont1+"</li>");

		inst.fadeOut();
		inst.attr({'data-role':" "});
		//inst.addClass();
		var fixid=fix.substring(4);
		//var currpow=ggpapa.attr('data-pstatus');
		for (var i = 0; i <11; i++) {
				temprole=ggpapa.children(".item"+fixid).eq(i).attr("data-role");
				//alert(temprole);

				if(temprole=="rolebowl")
				{
					rbowl++;
					temprole=null;
				}
				if(temprole=="rolebat")
				{
					rbat++;
					temprole=null;
				}
				if(temprole=="roleallround")
				{
					rall++;
					temprole=null;
				}
				if(temprole=="rolewk")
				{
					rwk++;
					temprole=null;
				}
			};
			
			
			var fncall=plych(rbowl,rbat,rwk,rall,fixid);
			rbat=0;rwk=0;rbowl=0;rall=0;


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
			//alert(newfix);
			$(".pow"+newfix).removeClass("ntd");
			$(".pow"+newfix).addClass("done");
		};
		if (state==1 && powstate==1) // selected player is power player
		{
			current.removeClass("powactive");
			currentpar.removeClass("paparent");
			current.attr({'data-pow':0});
			ggpapapow.attr({'data-pstatus':0});
			//fix=fix.substring(4);
			//alert(newfix);
			$(".pow"+newfix).addClass("ntd");
			$(".pow"+newfix).removeClass("done");
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
	var lockstate=0;
	$('.lockteam').click(function(){
		var check=storepl();

	});
	
});
