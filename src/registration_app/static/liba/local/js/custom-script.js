$(document).ready(function(){



//



//    Accordion/Toggle active title



//



    jQuery('.accordions').each(function(){



        var parent = jQuery(this);



        jQuery('.accordions .panel-heading a[data-toggle="collapse"]').on('click', function () {



            parent.find(jQuery('.panel-heading a[data-toggle="collapse"]')).removeClass('active');



            jQuery(this).addClass('active');



        });



    });



    jQuery('.toggles').each(function(){



        jQuery('.toggles .panel-heading a[data-toggle="collapse"]').on('click', function () {



            jQuery(this).toggleClass('active');



        });



    });







//



//    Top Menu change class on home page



//



    if($('.home').length){



        var window_hight = jQuery('#navbar-top').height();



        jQuery('.navbar-toggle').bind('click', function(){



            var value = jQuery(window).scrollTop();



            if ( value < (window_hight + 50) ){



                $("#navbar-top").toggleClass('nav-transparent');
				$("#navbar-top").toggleClass('nav-slide');


            }



        });



        jQuery(window).on('scroll', function () {



            var value = jQuery(window).scrollTop();



            if ( value < (window_hight + 50) ){



                if(jQuery('.navbar-collapse').hasClass('in') ==0){



                    $("#navbar-top").addClass('nav-transparent');
					$("#navbar-top").removeClass('nav-slide');


                }



            } else {



                $("#navbar-top").removeClass('nav-transparent');
				$("#navbar-top").addClass('nav-slide');



            }



        })



    }











//



//    Dropdown second level



//



    jQuery(".dropdown-menu > li > a.trigger").on("click",function(e){



        var current=jQuery(this).next();



        var grandparent=jQuery(this).parent().parent();



        grandparent.find(".dropdown-menu:visible").not(current).hide();



        jQuery('.dropdown-menu > li > a').removeClass('focus');



        jQuery(this).addClass('focus');



        current.toggle();



        e.stopPropagation();



    });



    jQuery(".dropdown-menu > li > a:not(.trigger)").on("click",function(){



        var root=jQuery(this).closest('.dropdown');



        jQuery('.dropdown-menu > li > a').removeClass('focus');



        root.find('.dropdown-menu:visible').hide();



    });



    



    



//  Lazy loading



    jQuery('img.lazy').lazy({



        effect : 'fadeIn',



        effectTime: 2000



    });



        



//  Circular progress bars



    $('.easyPieChart').each(function(){



        t = $(this);



        t.easyPieChart({



            animate:2300,



            lineCap:"round",



            lineWidth:t.attr("data-lineWidth"),



            size:175,



            barColor:t.attr("data-barColor"),



            trackColor:t.attr("data-trackColor"),



            scaleColor:"transparent",



        });



    });







    if(jQuery('.tp-banner').length){



        jQuery('.tp-banner').revolution(



            {



                delay:15000,



                startwidth:1170,



                startheight:500,



                hideThumbs:10,



                fullWidth:"off",



                fullScreen:"on",



                fullScreenOffsetContainer: "",



                navigationType: 'none',



                navigationStyle: 'square'



            });



    }



});







jQuery(window).load(function(){



    if(jQuery('.portfolio-section').length){



        var $container = $('.portfolio-items-list');







        $container.isotope({



            itemSelector : '.portfolio-item',



            resizable: true, // disable normal resizing



            transformsEnabled: true,



            masonry: { columnWidth: '1' }



        });







        $('.portfolio-filter a').click(function(){



            $('.portfolio-filter a').removeClass('active');



            $(this).addClass('active');



            var selector = $(this).attr('data-filter');



            $container.isotope({ filter: selector });



            return false;



        });



    }



    portfolioSection();



    jQuery(window).resize(function(){



        portfolioSection();



    })



})







    function portfolioSection(){



        if(jQuery('#portfolio').length){



            var dataStorage = function() {



                var el = {};



            }



            var container = $('#portfolio .portfolio');



            var container_top = $('#portfolio').offset().top;



            var headerH = $('#navbar-top').height();







            $('.portfolio-items-list .figure-hover-overlay').on('click', function(){



                var item = $('.item .' + $(this).parent().data('item'));



                item.css({position: 'relative'});



                container.fadeOut(1000, function(){



                    $('#portfolio .portfolio-wrap,.slide-nav').fadeIn(800);



                });



                $('html, body').animate({



                    scrollTop: (container_top - headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });



                item.show();



                item.animate({left: 0}, 1000);



                $('').show();



                dataStorage.el = this;



            });







            $('.portfolio-close').on('click', function(){



                $('#portfolio .portfolio-wrap, .slide-nav').fadeOut(1000, function(){



                    container.fadeIn(800);



                });



                var shown = $(dataStorage.el).parent().data('item');



                $('.'+shown).fadeOut(1000);



                $('html, body').animate({



                    scrollTop: (container_top - headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });



                return false;



            });







            $('.portfolio-next').on('click', function(){



                var currentEl = $(dataStorage.el).parent().data('item');



                var next = $(dataStorage.el).parent().next('.portfolio-item');



                if(next.length === 0) {



                    next = $('.portfolio-items-list .portfolio-item:first');



                    $('.item').css({left: -2000});



                }



                var nextData = next.data('item');

				$('.'+currentEl).fadeOut("slow");

                //$('.'+currentEl).animate({left: -2000}, 1000);



                /*$('.'+currentEl).hide();



                $('.'+nextData).show();*/



//                $('.'+nextData).animate({left: 0}, 1000);

				$('.'+nextData).fadeIn(3000);

				$('.'+nextData).css('left','0');

                dataStorage.el = next.find('figure');



                /*$('html, body').animate({



                    scrollTop: (container_top - headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });*/



                return false;



            });



            $('.portfolio-prev').on('click', function(){



                var currentEl = $(dataStorage.el).parent().data('item');



                var prev = $(dataStorage.el).parent().prev();



                if(prev.length === 0) {



                    prev = $('.portfolio-items-list .portfolio-item:last');



                    $('.item').css({left: 2000});



                }



                var prevData = prev.data('item');



                $('.'+currentEl).fadeOut("slow");



                //$('.'+currentEl).hide();



                //$('.'+prevData).show();



//                $('.'+prevData).animate({left: 0}, 1000);

				$('.'+prevData).fadeIn(3000);

				$('.'+prevData).css('left','0');



                dataStorage.el = prev.find('figure');



                /*$('html, body').animate({



                    scrollTop: (container_top - headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });*/



                return false;



            });



        }

        if (jQuery('#slider-portfolio').length) {



            var slider_dataStorage = function () {



                var el = {};



            }



            var slider_container = $('#slider-portfolio .slider-portfolio');



            var slider_container_top = $('#slider-portfolio').offset().top;



            var slider_headerH = $('#navbar-top').height();







            $('.slider-portfolio-items-list .slider-figure-hover-overlay').on('click', function () {



                var item = $('.slider-item .' + $(this).parent().data('item'));



                item.css({ position: 'relative' });



                slider_container.fadeOut(1000, function () {



                    $('#slider-portfolio .slider-wrap-portfolio, .slider-slide-nav').fadeIn(800);



                });



                $('html, body').animate({



                    scrollTop: (slider_container_top - slider_headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });



                item.show();



                item.animate({ left: 0 }, 1000);



                $('').show();



                slider_dataStorage.el = this;



            });







            $('.slider-portfolio-close').on('click', function () {



                $('#slider-portfolio .slider-wrap-portfolio, .slider-slide-nav').fadeOut(1000, function () {



                    slider_container.fadeIn(800);



                });



                var shown = $(slider_dataStorage.el).parent().data('item');



                $('.' + shown).fadeOut(1000);



                $('html, body').animate({



                    scrollTop: (slider_container_top - slider_headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });



                return false;



            });







            $('.slider-portfolio-next').on('click', function () {


				$(".slider-hide").hide();
                var currentEl = $(slider_dataStorage.el).parent().data('item');



                var next = $(slider_dataStorage.el).parent().next('.slider-portfolio-item');



                if (next.length === 0) {



                    next = $('.slider-portfolio-items-list .slider-portfolio-item:first');



                    $('.slider-item').css({ left: -2000 });



                }



                var nextData = next.data('item');

                /*$('.' + currentEl).fadeOut("fast",function(){
					debugger;
					$('.' + nextData).css('left', '0');
					$('.' + nextData).fadeIn(3000);
				});*/

				$('.' + currentEl).fadeOut('slow');
				
				$('.' + nextData).fadeIn(1000);
				$('.' + nextData).css('left', '0');
                //$('.'+currentEl).animate({left: -2000}, 1000);



                /*$('.'+currentEl).hide();



                $('.'+nextData).show();*/



                //                $('.'+nextData).animate({left: 0}, 1000);

                

                

                slider_dataStorage.el = next.find('figure');



                /*$('html, body').animate({



                    scrollTop: (container_top - headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });*/



                return false;



            });



            $('.slider-portfolio-prev').on('click', function () {

				
				$(".slider-hide").hide();
                var currentEl = $(slider_dataStorage.el).parent().data('item');



                var prev = $(slider_dataStorage.el).parent().prev();



                if (prev.length === 0) {



                    prev = $('.slider-portfolio-items-list .slider-portfolio-item:last');



                    $('.slider-item').css({ left: 2000 });



                }



                var prevData = prev.data('item');



                /*$('.' + currentEl).fadeOut("fast",function(){
					debugger;
					$('.' + prevData).css('left', '0');
					$('.' + prevData).fadeIn(3000);
					
				});*/

				$('.' + currentEl).fadeOut('slow');
				$('.' + prevData).fadeIn(1000);
				$('.' + prevData).css('left', '0');
				

                //$('.'+currentEl).hide();



                //$('.'+prevData).show();



                //                $('.'+prevData).animate({left: 0}, 1000);

                

                



                slider_dataStorage.el = prev.find('figure');



                /*$('html, body').animate({



                    scrollTop: (container_top - headerH - 15) + "px"



                }, {



                    duration: 1200,



                    easing: "easeInOutExpo"



                });*/



                return false;



            });



        
		
	}

    }


