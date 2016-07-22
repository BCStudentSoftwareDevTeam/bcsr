
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
        $(".hamburger").animate({ left: 30});
        isClosed = false;
      } else {   
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        $(".hamburger").animate({ left: 230});
        isClosed = true;
      }
  }
  

  $('[data-toggle="offcanvas"]').click(function (evt) {
        $('#wrapper').toggleClass('toggled');
        evt.stopImmediatePropagation();
  });  
  
  var isCollapsed;
  $('.navbar-toggle').click(function (evt) {
    if(!isCollapsed){
    $(".hamburger").animate({ top: 250 })
    $("#sidebar-wrapper").animate({top: 180})
    } else {
      $(".hamburger").animate({ top: 70 })
      $("#sidebar-wrapper").animate({top: 0})
    }
    
    isCollapsed = !isCollapsed;
  });
});

function toggleArrowIcon(iconID,labelID) {
	console.log(iconID);
	console.log(labelID);
	$(iconID).toggleClass('glyphicon-menu-down');
	toggleLabel(labelID);
}

function toggleLabel(labelID) {
	$(labelID).parent().children('ul.tree').toggle(300);
}

