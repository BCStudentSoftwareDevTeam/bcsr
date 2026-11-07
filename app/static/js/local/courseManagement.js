$("#number").on("input", function(){
    this.value = this.value.replace(/ /g, "");
    if (this.value && /\D/.test(this.value)) {
        this.setCustomValidity("Please enter numbers only.");
        this.reportValidity();
    } else {this.setCustomValidity("");}
    });