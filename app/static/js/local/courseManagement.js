$("#number").on("input", function(){
    if ($(this).val() && isNaN($(this).val())) {
        this.setCustomValidity("Please enter numbers only.");
        this.reportValidity();
    } else {this.setCustomValidity("");}
    this.value = this.value.replace(/ /g, "");});