    /* global $ */
    function showPrograms(division) {
    var programID = '#programs-'+ division;
    if($(programID).css('display') == 'none'){
        $(programID).css('display', 'block');
        
        
    } else {
        $(programID).css('display', 'none');
    }
    
    $('#icon-'+ division).toggleClass('glyphicon-plus')
    $('#icon-'+ division).toggleClass('glyphicon-minus')
}


function showCourses(program) {
    var programID = '#courses-'+ program;
    if($(programID).css('display') == 'none'){
        $(programID).css('display', 'block');
        
        
    } else {
        $(programID).css('display', 'none');
    }
    
    $('#coursesIcon-'+ program).toggleClass('glyphicon-plus')
    $('#coursesIcon-'+ program).toggleClass('glyphicon-minus')
}