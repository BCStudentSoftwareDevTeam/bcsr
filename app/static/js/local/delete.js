function gen_card(filepath){
  let grid = $("<div>", {"class": "col-md-4"});
  let thumbnail = $("<div>", {"class":"thumbnail"})
  let link = $("<a>", {"href": filepath})
  let image = $("<img>", {"class": "img-thumbnail", "src": "/static/img/document_icon.svg"})
  let rm_button = $("<button>", {"data-div":"TEST_DATA", "type":"button", "class": "center-block btn btn-danger  btn-sm"})
  let trash_icon = $("<span>", {"class":"glyphicon glyphicon-trash","text": "Delete"})

  grid.append(
    thumbnail.append(
      link.append(
        image.append(),
        rm_button.append(
          trash_icon
        )
      )
    )
  )
  
  $("#BODY").append(grid) 
}
