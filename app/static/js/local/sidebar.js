
$(document).ready(function () {
  var trigger = $('.hamburger'),
      overlay = $('.overlay'),
     isClosed = false;

    trigger.click(function () {
      hamburger_cross();      
    });
// position the hamburger and show. Needed so that the hamburger is positioned correctly
$(".hamburger").offset({ top: 70, left: 30});
$(".hamburger").show()
    function hamburger_cross() {

      if (isClosed == true) {          
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        $(".hamburger").stop().animate({ left: 30});
        isClosed = false;
      } else {   
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        $(".hamburger").stop().animate({ left: 230});
        isClosed = true;
      }
  }
  
  var animateDown = function() {
     $(".hamburger").animate({ top: 250 })
    $("#sidebar-wrapper").animate({top: 180})
  };
  
  var animateUp = function() {
    $(".hamburger").animate({ top: 70 })
      $("#sidebar-wrapper").stop().animate({top: 0})
  };
  $('[data-toggle="offcanvas"]').click(function (evt) {
        $('#wrapper').toggleClass('toggled');
        evt.stopImmediatePropagation();
  });  
  
  var moveHamburger = function(isNavCollapsed) {
    if(isNavCollapsed){
      animateUp()
    } else {
      animateDown()
    }
  }
  
  var isCollapsed = true;
  $('.navbar-toggle').click(function (evt) {
    moveHamburger(!isCollapsed);
    isCollapsed = !isCollapsed;
  });
 
});

function toggleArrowIcon(iconID,labelID) {
	$(iconID).toggleClass('glyphicon-menu-down');
	toggleLabel(labelID);
}

function toggleLabel(labelID) {
	$(labelID).parent().children('ul.tree').toggle(300);
}

