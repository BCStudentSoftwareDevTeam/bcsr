// $(document).ready(function(){
//     $('.classloader').click(function(){
//         $('.contenthere').load("{{division.DID}}");
//     });
// })
/* global $ */

$(document).ready(function(){
  $("span#icon-{{division.DID}}").removeClass("hidden");
});
function showPrograms(division) {
var divisionID = '#divisions'
if($(divisionID).css('display') == 'none'){
    $(divisionID).css('display', 'block');

} else {
    $(divisionID).css('display', 'none');
}
});


// function divurl(){
//   document.getElementById("testdiv").onclick();
//   window.location.href="/courses/<"{{division.name}}">{{division.name}}";
// }
//
// function addElemId() {
//   var newId = document.getElementsByClassName("sidebar-nav");
//   for (n=0, length = newId.length; n < length; n++) {
//     newId[n].id= "division_"+ (n+1);
//     console.log("addElemId");
//   }
//
// };
