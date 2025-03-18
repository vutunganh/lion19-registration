// JavaScript Document
if($(this).width()<768){
	$(document).ready(function(){
	$('.bxslider').bxSlider({
		  minSlides: 1,
		  maxSlides: 1,
		  slideWidth: 263,
		  slideMargin: 0,
		});
	});
		
}  else if($(this).width()<991) {
   $(document).ready(function(){
	 $('.bxslider').bxSlider({
		  minSlides: 2,
		  maxSlides: 2,
		  slideWidth: 400,
		  slideMargin: 0,
		});
	  
	});
   
} else if($(this).width()>990) {
   $(document).ready(function(){
	$('.bxslider').bxSlider({
		  minSlides: 3,
		  maxSlides: 10,
		  slideWidth: 400,
		  slideMargin: 0,
		});
	});
   
}          