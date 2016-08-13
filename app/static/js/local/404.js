$(document).ready(function(){
  $('h2').css({ 'width':'100%', 'text-align':'center' });
  $('p').css({ 'width':'100%', 'text-align':'center' });
  var h2 = $('h2').height();
  var h = h2/2;
  var w1 = $(window).height();
  var w = w1/2;
  var m = w - h
  $('h2').css("top",(m-60) + "px")
  $('p').css("top", (m)+"px")
});