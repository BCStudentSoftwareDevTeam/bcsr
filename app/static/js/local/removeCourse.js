//TODO: I am having trouble looping through the json array
//Might have to create another function to retrieve and return the json
//data so that I can loop through the dictionary using javascript.
function getCourses(){
    var SEID = document.getElementById('SEID');
    console.log('This is SEID')
    console.log(SEID.value)
    if (SEID.value != 'None'){
        $('#courses').find('option').remove().end()
        addEmptyLine('Select a Course')
        var URL  = 'removeCourse/json/' + SEID.value;
        $.getJSON(URL, function (data){
            $.each(data,function(list,courses){
                $.each(JSON.parse(courses),function(element,course){
                    var optionText = course.title + ' ' + course.instructor
                    var optionValue = course.CID                            
                    $('#courses').append($('<option>', {
                        value: optionValue,
                        text: optionText
                    }))
                })
            })
        $('#courses').selectpicker('refresh');
        })
        
    } else {
        $('#courses').find('option').remove()
        addEmptyLine('Select a Semester')
        $('#courses').selectpicker('refresh')
    }
}

function addEmptyLine(textVal){
    $("#courses").append($('<option>', {
        value: '',
        text: textVal
    }))
}